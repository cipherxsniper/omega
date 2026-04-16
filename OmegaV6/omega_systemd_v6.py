import os
import json
import time
import signal
import threading
import subprocess
from collections import defaultdict

# ---------------------------
# GLOBAL SHUTDOWN FLAG
# ---------------------------

RUNNING = True

def shutdown_signal(sig, frame):
    global RUNNING
    print("\n[V6] SHUTDOWN SIGNAL RECEIVED")
    RUNNING = False

signal.signal(signal.SIGINT, shutdown_signal)
signal.signal(signal.SIGTERM, shutdown_signal)

# ---------------------------
# LOGGING
# ---------------------------

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} [V6] {msg}")

# ---------------------------
# LAUNCHER
# ---------------------------

def launch(service):
    return subprocess.Popen(
        ["python", "omega_service_agent_v6.py", service]
    )

# ---------------------------
# KERNEL V6
# ---------------------------

class OmegaSystemDV6:

    def __init__(self, manifest):
        self.services = manifest.get("services", {})

        self.graph = defaultdict(list)
        self.state = {}
        self.processes = {}

        self.build_graph()

    # -----------------------
    # DEP GRAPH
    # -----------------------

    def build_graph(self):
        for svc, cfg in self.services.items():
            self.graph[svc] = cfg.get("requires", [])
            self.state[svc] = "PENDING"

    # -----------------------
    # START SERVICE
    # -----------------------

    def start(self, svc):
        if svc in self.processes:
            return

        log(f"START → {svc}")

        self.processes[svc] = {
            "proc": launch(svc),
            "restarts": 0,
            "last": time.time()
        }

        self.state[svc] = "ACTIVE"

    # -----------------------
    # STOP SERVICE
    # -----------------------

    def stop_all(self):
        log("STOPPING ALL SERVICES")

        for svc, meta in self.processes.items():
            try:
                meta["proc"].terminate()
            except:
                pass

        self.processes.clear()

    # -----------------------
    # DEP CHECK
    # -----------------------

    def deps_ok(self, svc):
        for d in self.graph[svc]:
            if self.state.get(d) != "ACTIVE":
                return False
        return True

    # -----------------------
    # MONITOR LOOP
    # -----------------------

    def monitor(self):
        global RUNNING

        while RUNNING:
            time.sleep(2)

            for svc in self.services:

                if not self.deps_ok(svc):
                    self.state[svc] = "BLOCKED"
                    continue

                meta = self.processes.get(svc)

                if not meta:
                    self.start(svc)
                    continue

                proc = meta["proc"]

                if proc.poll() is not None:
                    log(f"DEAD → {svc}")

                    meta["restarts"] += 1

                    if meta["restarts"] > 3:
                        log(f"KILLED (max restarts) → {svc}")
                        self.state[svc] = "FAILED"
                        continue

                    self.start(svc)

                else:
                    self.state[svc] = "ACTIVE"

                log(f"{svc} → {self.state[svc]}")

        self.stop_all()
        log("KERNEL SHUTDOWN COMPLETE")

    # -----------------------
    # BOOT
    # -----------------------

    def boot(self):
        log("BOOT START")

        for svc in self.services:
            if self.deps_ok(svc):
                self.start(svc)

        log("BOOT COMPLETE")

        self.monitor()


# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":

    if not os.path.exists("omega_manifest.json"):
        log("MISSING MANIFEST")
        exit(1)

    manifest = json.load(open("omega_manifest.json"))

    OmegaSystemDV6(manifest).boot()
