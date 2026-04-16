import os
import time
import subprocess
from collections import defaultdict
from omega_manifest_loader_patch import load_manifest

LOG = "[OMEGA INIT]"

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")

# ---------------------------
# VERSION ENGINE
# ---------------------------

def base(name):
    return name.split("_v")[0] if "_v" in name else name.replace(".py","")

def version(name):
    try:
        if "_v" in name:
            return int(name.split("_v")[-1].split(".")[0])
    except:
        return 0
    return 0

def dedupe(services):
    grouped = defaultdict(list)

    for s in services:
        grouped[base(s)].append(s)

    return [max(v, key=version) for v in grouped.values()]

# ---------------------------
# SAFE LAUNCH
# ---------------------------

def launch(service):
    if not os.path.exists(service):
        log(f"⚠️ Missing: {service}")
        return None

    log(f"🚀 Launching: {service}")

    return subprocess.Popen(
        ["python", service],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

# ---------------------------
# OMEGA INIT SYSTEM
# ---------------------------

class OmegaInitSystem:

    def __init__(self, manifest):
        self.raw = manifest.get("services", [])
        self.services = dedupe(self.raw)
        self.processes = {}

    def boot(self):
        log("🔵 BOOT START")

        for s in self.services:
            self.start(s)

        log("🟢 SYSTEM ONLINE")
        self.monitor()

    def start(self, s):
        if s in self.processes:
            return

        p = launch(s)
        if p:
            self.processes[s] = {"p": p, "r": 0}

    def restart(self, s):
        meta = self.processes.get(s)
        if not meta:
            return

        if meta["r"] > 3:
            log(f"❌ KILLED (restarts exceeded): {s}")
            return

        log(f"🔁 Restarting: {s}")

        meta["p"].terminate()
        time.sleep(1)

        meta["p"] = launch(s)
        meta["r"] += 1

    def monitor(self):
        while True:
            time.sleep(3)

            for s, m in list(self.processes.items()):
                if m["p"].poll() is not None:
                    log(f"⚠️ DEAD: {s}")
                    self.restart(s)

            if not self.processes:
                log("❌ SYSTEM HALT")
                break


if __name__ == "__main__":
    manifest = load_manifest()
    if not manifest:
        exit(1)

    OmegaInitSystem(manifest).boot()
