import os
import json
import time
import socket
import threading
import subprocess
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 5050

# ---------------------------
# LOGGING
# ---------------------------

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} [V5] {msg}")

# ---------------------------
# SOCKET BUS
# ---------------------------

class SocketBus:
    def __init__(self):
        self.last_beat = {}
        self.latency = {}

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        log("BUS ONLINE")

        while True:
            conn, _ = s.accept()
            threading.Thread(target=self.handle, args=(conn,), daemon=True).start()

    def handle(self, conn):
        try:
            while True:
                data = conn.recv(2048).decode().strip()
                if not data:
                    break

                msg = json.loads(data)
                svc = msg["service"]
                ts = msg["ts"]

                now = time.time()
                self.last_beat[svc] = now
                self.latency[svc] = now - ts

        except:
            pass
        finally:
            conn.close()

# ---------------------------
# SERVICE AGENT LAUNCHER
# ---------------------------

def launch(service):
    return subprocess.Popen(
        ["python", "omega_service_agent_v5.py", service]
    )

# ---------------------------
# KERNEL V5
# ---------------------------

class OmegaSystemD5:

    def __init__(self, manifest):
        self.manifest = manifest

        self.services = manifest.get("services", {})
        self.graph = defaultdict(list)

        self.state = {}
        self.processes = {}

        self.bus = SocketBus()

        self.build_graph()

    # -----------------------
    # DEPENDENCY GRAPH
    # -----------------------

    def build_graph(self):
        for svc, cfg in self.services.items():
            deps = cfg.get("requires", [])
            self.graph[svc] = deps

            self.state[svc] = "BLOCKED" if deps else "PENDING"

    # -----------------------
    # START SERVICE
    # -----------------------

    def start(self, svc):
        log(f"START → {svc}")

        self.state[svc] = "STARTING"

        proc = launch(svc)

        self.processes[svc] = proc
        self.state[svc] = "ACTIVE"

    # -----------------------
    # CHECK DEPENDENCIES
    # -----------------------

    def deps_ok(self, svc):
        for dep in self.graph[svc]:
            if self.state.get(dep) != "ACTIVE":
                return False
        return True

    # -----------------------
    # MONITOR LOOP
    # -----------------------

    def monitor(self):
        while True:
            time.sleep(2)

            now = time.time()

            for svc in self.services:

                # BLOCKED BY DEPENDENCIES
                if not self.deps_ok(svc):
                    self.state[svc] = "BLOCKED"
                    continue

                last = self.bus.last_beat.get(svc)

                if not last:
                    self.state[svc] = "DEGRADED"
                    continue

                age = now - last

                if age > 6:
                    self.state[svc] = "FAILED"

                    log(f"FAILED → {svc}")

                    proc = self.processes.get(svc)
                    if proc:
                        proc.terminate()

                    self.start(svc)

                elif age > 3:
                    self.state[svc] = "DEGRADED"
                else:
                    self.state[svc] = "ACTIVE"

                log(f"{svc} → {self.state[svc]} (age={round(age,2)})")

    # -----------------------
    # BOOT SEQUENCE
    # -----------------------

    def boot(self):
        log("BOOT START")

        threading.Thread(target=self.bus.start, daemon=True).start()
        time.sleep(1)

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

    OmegaSystemD5(manifest).boot()
