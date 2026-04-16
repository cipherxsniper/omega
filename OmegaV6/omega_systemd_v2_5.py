import os
import time
import json
import traceback
from collections import defaultdict
from omega_launch_guard import safe_launch

LOG = "[OMEGA v2.5]"

# ---------------------------
# LOGGING (JOURNALD STYLE)
# ---------------------------
def log(level, msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} [{level}] {msg}")

# ---------------------------
# LOAD MANIFEST
# ---------------------------
def load_manifest():
    path = "omega_manifest.json"

    if not os.path.exists(path):
        log("ERROR", "Missing manifest")
        return None

    with open(path) as f:
        return json.load(f).get("services", {})

# ---------------------------
# DAG RESOLUTION
# ---------------------------
def resolve_dag(services):
    visited = set()
    order = []

    def visit(node):
        if node in visited:
            return
        visited.add(node)

        for dep in services.get(node, []):
            visit(dep)

        order.append(node)

    for s in services:
        visit(s)

    return order

# ---------------------------
# PREFLIGHT VALIDATION
# ---------------------------
def preflight(service):
    if not os.path.exists(service):
        return False, "MISSING_FILE"

    try:
        with open(service) as f:
            content = f.read()

        if "while True" not in content and "sleep" not in content:
            return False, "NO_RUNTIME_LOOP"

        return True, "OK"

    except Exception as e:
        return False, str(e)

# ---------------------------
# CRASH CLASSIFIER
# ---------------------------
def classify(proc):
    if proc is None:
        return "FAILED_TO_START"

    code = proc.poll()

    if code is None:
        return "RUNNING"

    if code == 0:
        return "CLEAN_EXIT"

    return "NON_ZERO_EXIT"

# ---------------------------
# SYSTEMD CORE
# ---------------------------
class OmegaSystemD25:

    def __init__(self, services):
        self.services = services
        self.order = resolve_dag(services)
        self.procs = {}
        self.meta = {}
        self.disabled = set()

    def boot(self):
        log("INFO", "BOOT START")
        log("INFO", f"ORDER: {self.order}")

        for s in self.order:
            self.start(s)

        log("INFO", "BOOT COMPLETE")
        self.monitor()

    def start(self, s):
        if s in self.disabled:
            return

        ok, reason = preflight(s)

        if not ok:
            log("BLOCK", f"{s} → PREFLIGHT FAIL ({reason})")
            self.disabled.add(s)
            return

        proc = safe_launch(s)

        if not proc:
            log("FAIL", f"{s} → FAILED TO START")
            self.disabled.add(s)
            return

        self.procs[s] = proc
        self.meta[s] = {"restarts": 0, "state": "ACTIVE"}

        log("INFO", f"{s} → ACTIVE")

    def restart(self, s):
        if s in self.disabled:
            return

        m = self.meta[s]

        if m["restarts"] >= 3:
            log("BLOCK", f"{s} → TOO MANY RESTARTS")
            self.disabled.add(s)
            return

        log("INFO", f"{s} → RESTARTING")

        proc = safe_launch(s)

        if not proc:
            log("FAIL", f"{s} → RESTART FAILED")
            self.disabled.add(s)
            return

        self.procs[s] = proc
        m["restarts"] += 1

    def monitor(self):
        while True:
            time.sleep(2)

            for s, proc in list(self.procs.items()):
                state = classify(proc)

                if state == "RUNNING":
                    log("OK", f"{s} → ACTIVE")
                    continue

                log("WARN", f"{s} → DEAD ({state})")
                self.restart(s)

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    services = load_manifest()

    if not services:
        exit()

    OmegaSystemD25(services).boot()
