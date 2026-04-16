import os
import time
import json
import socket
import threading
import subprocess
from collections import defaultdict

LOG = "[OMEGA SYSTEMD v6]"

# -------------------------
# LOGGING
# -------------------------
def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")

# -------------------------
# SERVICE DISCOVERY
# -------------------------
def discover_services():
    return [f for f in os.listdir(".") if f.endswith(".py")]

# -------------------------
# SERVICE CONTRACTS
# -------------------------
def load_contract(service):
    return {
        "name": service,
        "heartbeat": 2,
        "max_restarts": 3,
        "deps": []
    }

# -------------------------
# IPC BUS (SOCKET)
# -------------------------
class IPCBus:

    def __init__(self, port=5050):
        self.port = port
        self.subscribers = []
        self.running = True

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        log("📡 IPC BUS ONLINE")

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", self.port))
        s.listen(10)

        while self.running:
            conn, _ = s.accept()
            data = conn.recv(4096).decode()
            self.broadcast(data)
            conn.close()

    def broadcast(self, msg):
        log(f"📡 BUS MSG → {msg}")

# -------------------------
# SWARM HEALER
# -------------------------
class SwarmHealer:

    def classify(self, service, proc):

        if proc.returncode == 0:
            return "OK"

        if proc.returncode == 1:
            return "FAIL_FAST"

        if proc.returncode == 2:
            return "IMPORT_FAIL"

        return "UNKNOWN_CRASH"

# -------------------------
# CONTROL PLANE
# -------------------------
class OmegaSystemD6:

    def __init__(self):
        self.services = discover_services()
        self.processes = {}
        self.restarts = defaultdict(int)
        self.contracts = {s: load_contract(s) for s in self.services}
        self.bus = IPCBus()
        self.healer = SwarmHealer()

    # ---------------------
    # START SERVICE
    # ---------------------
    def start(self, service):

        contract = self.contracts[service]

        if self.restarts[service] >= contract["max_restarts"]:
            log(f"🧊 ISOLATED → {service}")
            return

        log(f"🚀 START → {service}")

        proc = subprocess.Popen(
            ["python", service],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.processes[service] = proc

    # ---------------------
    # RESTART POLICY
    # ---------------------
    def restart(self, service, reason):

        self.restarts[service] += 1

        log(f"🔁 RESTART → {service} ({reason})")

        self.start(service)

    # ---------------------
    # MONITOR LOOP
    # ---------------------
    def monitor(self):

        while True:
            time.sleep(2)

            for service, proc in list(self.processes.items()):

                if proc.poll() is not None:

                    reason = self.healer.classify(service, proc)

                    log(f"💀 DEAD → {service} | {reason}")

                    if reason == "IMPORT_FAIL":
                        log(f"🧠 CONTRACT VIOLATION → {service}")

                    if reason in ["FAIL_FAST", "UNKNOWN_CRASH"]:
                        self.restart(service, reason)

    # ---------------------
    # BOOT
    # ---------------------
    def boot(self):

        log("🧠 BOOT START")

        self.bus.start()

        for s in self.services:
            self.start(s)

        log("🟢 BOOT COMPLETE")

        self.monitor()

# -------------------------
# ENTRY
# -------------------------
if __name__ == "__main__":
    OmegaSystemD6().boot()
