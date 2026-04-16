import os
import json
import time
import signal
import subprocess
from collections import defaultdict, deque

# =========================================================
# 🧠 OMEGA SYSTEMD V7 — CONTROL PLANE KERNEL
# =========================================================

MANIFEST = "omega_manifest.json"

RUNNING = True

# -------------------------
# JOURNALD EVENT BUS
# -------------------------

class Journal:
    def __init__(self):
        self.events = []

    def log(self, level, service, msg, meta=None):
        event = {
            "ts": time.time(),
            "level": level,
            "service": service,
            "msg": msg,
            "meta": meta or {}
        }
        self.events.append(event)
        print(f"[JOURNAL:{level}] {service} → {msg}")

journal = Journal()

# -------------------------
# SIGNAL HANDLER
# -------------------------

def shutdown(sig, frame):
    global RUNNING
    journal.log("INFO", "SYSTEM", "SHUTDOWN SIGNAL RECEIVED")
    RUNNING = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# -------------------------
# SERVICE LAUNCHER
# -------------------------

def launch(service):
    return subprocess.Popen(
        ["python", service],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# -------------------------
# CRASH INTELLIGENCE ENGINE
# -------------------------

def classify_crash(meta):
    if meta.get("restart_count", 0) > 3:
        return "RESTART_LIMIT_EXCEEDED"
    if meta.get("last_runtime", 0) < 0.5:
        return "INSTANT_EXIT"
    if meta.get("last_exit_code", 0) != 0:
        return "NON_ZERO_EXIT"
    return "UNKNOWN_CRASH"

# -------------------------
# SYSTEMD V7 KERNEL
# -------------------------

class OmegaSystemDV7:

    def __init__(self, manifest):
        self.services = manifest.get("services", {})
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)

        self.processes = {}
        self.state = {}

        self.build_graph()

    # ---------------------
    # BUILD DEP GRAPH (DAG)
    # ---------------------

    def build_graph(self):
        for svc, cfg in self.services.items():
            deps = cfg.get("requires", [])
            self.graph[svc] = deps
            self.state[svc] = "PENDING"

            for d in deps:
                self.reverse_graph[d].append(svc)

    # ---------------------
    # TOPO SORT BOOT ORDER
    # ---------------------

    def resolve_boot_order(self):
        indeg = {s: 0 for s in self.services}
        for s in self.services:
            for d in self.graph[s]:
                indeg[s] += 1

        q = deque([s for s in indeg if indeg[s] == 0])
        order = []

        while q:
            n = q.popleft()
            order.append(n)

            for child in self.reverse_graph[n]:
                indeg[child] -= 1
                if indeg[child] == 0:
                    q.append(child)

        return order

    # ---------------------
    # START SERVICE
    # ---------------------

    def start(self, svc):
        if svc in self.processes:
            return

        journal.log("INFO", svc, "STARTING")

        proc = launch(svc)

        self.processes[svc] = {
            "proc": proc,
            "restart_count": 0,
            "start_time": time.time(),
            "last_exit_code": None
        }

        self.state[svc] = "ACTIVE"

    # ---------------------
    # RESTART LOGIC
    # ---------------------

    def restart(self, svc):
        meta = self.processes.get(svc)
        if not meta:
            return

        meta["restart_count"] += 1

        crash_type = classify_crash(meta)

        journal.log("WARN", svc, f"CRASH DETECTED: {crash_type}")

        if meta["restart_count"] > 3:
            self.state[svc] = "DISABLED"
            journal.log("BLOCK", svc, "SERVICE DISABLED (restart limit)")
            return

        journal.log("INFO", svc, "RESTARTING")

        try:
            meta["proc"].terminate()
        except:
            pass

        time.sleep(1)

        proc = launch(svc)

        meta["proc"] = proc
        meta["start_time"] = time.time()

        self.state[svc] = "RESTARTING"

    # ---------------------
    # HEALTH CHECK
    # ---------------------

    def check(self, svc, meta):
        proc = meta["proc"]

        if proc.poll() is not None:
            meta["last_exit_code"] = proc.poll()
            return False

        runtime = time.time() - meta["start_time"]
        meta["last_runtime"] = runtime

        if runtime > 1:
            self.state[svc] = "ACTIVE"
        else:
            self.state[svc] = "DEGRADED"

        return True

    # ---------------------
    # MONITOR LOOP
    # ---------------------

    def monitor(self):
        global RUNNING

        while RUNNING:
            time.sleep(2)

            for svc, meta in list(self.processes.items()):

                if not self.check(svc, meta):
                    journal.log("WARN", svc, "DEAD")
                    self.restart(svc)
                    continue

                journal.log("INFO", svc, self.state[svc])

        self.shutdown()

    # ---------------------
    # SHUTDOWN CLEANUP
    # ---------------------

    def shutdown(self):
        journal.log("INFO", "SYSTEM", "SHUTTING DOWN")

        for svc, meta in self.processes.items():
            try:
                meta["proc"].terminate()
            except:
                pass

        journal.log("INFO", "SYSTEM", "KERNEL HALTED")

    # ---------------------
    # BOOT SEQUENCE
    # ---------------------

    def boot(self):
        journal.log("INFO", "SYSTEM", "BOOT START")

        order = self.resolve_boot_order()

        journal.log("INFO", "SYSTEM", f"BOOT ORDER: {order}")

        for svc in order:
            self.start(svc)

        journal.log("INFO", "SYSTEM", "BOOT COMPLETE")

        self.monitor()


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":

    if not os.path.exists(MANIFEST):
        print("[FATAL] missing manifest")
        exit(1)

    manifest = json.load(open(MANIFEST))

    OmegaSystemDV7(manifest).boot()
