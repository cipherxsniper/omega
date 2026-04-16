import os
import json
import time
import subprocess
from collections import defaultdict

MANIFEST_FILE = "omega_manifest.json"
LOG_PREFIX = "[OMEGA INIT]"

# ---------------------------
# UTILITIES
# ---------------------------

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG_PREFIX} {msg}")

def load_manifest():
    if not os.path.exists(MANIFEST_FILE):
        log("❌ Missing manifest file")
        return None

    with open(MANIFEST_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            log("❌ Invalid manifest JSON")
            return None

# ---------------------------
# VERSION RESOLUTION ENGINE
# ---------------------------

def extract_base(name):
    """
    omega_kernel_v47.py -> omega_kernel
    """
    if "_v" in name:
        return name.split("_v")[0]
    return name.replace(".py", "")

def extract_version(name):
    try:
        if "_v" in name:
            part = name.split("_v")[-1]
            return int(part.split(".")[0])
    except:
        pass
    return 0

def deduplicate_services(services):
    grouped = defaultdict(list)

    for s in services:
        base = extract_base(s)
        grouped[base].append(s)

    selected = []

    for base, items in grouped.items():
        best = max(items, key=extract_version)
        selected.append(best)

    return selected

# ---------------------------
# DEPENDENCY GRAPH BUILDER
# ---------------------------

def build_graph(services):
    graph = defaultdict(list)

    for i in range(len(services)):
        if i + 1 < len(services):
            graph[services[i]].append(services[i + 1])

    return graph

# ---------------------------
# SAFE LAUNCHER (NO SPAM SPAWN)
# ---------------------------

def launch_service(name):
    if not os.path.exists(name):
        log(f"⚠️ Missing service: {name}")
        return None

    log(f"🚀 Starting service: {name}")

    return subprocess.Popen(
        ["python", name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ---------------------------
# SYSTEMD-LIKE CONTROLLER
# ---------------------------

class OmegaInitSystem:

    def __init__(self, manifest):
        self.raw_services = manifest.get("services", [])
        self.services = deduplicate_services(self.raw_services)
        self.graph = build_graph(self.services)
        self.processes = {}

    def boot(self):
        log("🔵 INIT START")

        for service in self.services:
            self.start(service)

        log("🟢 SYSTEM ONLINE")

        self.monitor()

    def start(self, service):
        if service in self.processes:
            log(f"⏭️ Already running: {service}")
            return

        proc = launch_service(service)
        if proc:
            self.processes[service] = {
                "proc": proc,
                "last_restart": time.time(),
                "restarts": 0
            }

    def restart(self, service):
        meta = self.processes.get(service)
        if not meta:
            return

        if meta["restarts"] > 3:
            log(f"❌ STOPPING (too many restarts): {service}")
            return

        log(f"🔁 Restarting: {service}")

        meta["proc"].terminate()
        time.sleep(1)

        proc = launch_service(service)

        meta["proc"] = proc
        meta["restarts"] += 1
        meta["last_restart"] = time.time()

    def monitor(self):
        while True:
            time.sleep(3)

            for service, meta in list(self.processes.items()):
                proc = meta["proc"]

                if proc.poll() is not None:
                    log(f"⚠️ DEAD: {service}")
                    self.restart(service)

            if len(self.processes) == 0:
                log("❌ NO ACTIVE SERVICES → SYSTEM HALT")
                break


# ---------------------------
# MAIN ENTRY
# ---------------------------

if __name__ == "__main__":
    manifest = load_manifest()
    if not manifest:
        exit(1)

    system = OmegaInitSystem(manifest)
    system.boot()
