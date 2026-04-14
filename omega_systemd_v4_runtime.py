import os
import time
import json
import socket
import subprocess
import threading

LOG = "[OMEGA SYSTEMD v4]"

HEARTBEAT_PORT = 5050
HEARTBEAT_INTERVAL = 2

# ----------------------------
# LOGGING
# ----------------------------
def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG} {msg}")

# ----------------------------
# SERVICE CONTRACT LOADER
# ----------------------------
def load_contract(service):
    try:
        with open(service, "r") as f:
            code = f.read()

        return {
            "is_daemon": "while True" in code,
            "has_heartbeat": "send_heartbeat" in code,
        }
    except:
        return {"is_daemon": False, "has_heartbeat": False}

# ----------------------------
# HEARTBEAT SERVER
# ----------------------------
class HeartbeatBus:

    def __init__(self):
        self.state = {}

    def start(self):
        t = threading.Thread(target=self.listen, daemon=True)
        t.start()

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("127.0.0.1", HEARTBEAT_PORT))

        log("📡 HEARTBEAT BUS ONLINE")

        while True:
            data, addr = s.recvfrom(1024)
            msg = data.decode()

            try:
                service, ts = msg.split("|")
                self.state[service] = time.time()
            except:
                pass

    def check(self, service):
        last = self.state.get(service)
        if not last:
            return "DEAD"

        if time.time() - last > 6:
            return "STALE"

        return "ACTIVE"

# ----------------------------
# SERVICE RUNTIME
# ----------------------------
class ServiceRuntime:

    def __init__(self, bus):
        self.bus = bus
        self.processes = {}
        self.restarts = {}

    def start(self, service):

        contract = load_contract(service)

        if len(self.processes) >= 10:
            log("⚠️ MAX CAPACITY REACHED")
            return

        if not os.path.exists(service):
            log(f"⚠️ MISSING → {service}")
            return

        log(f"🚀 START → {service} | daemon={contract['is_daemon']}")

        proc = subprocess.Popen(
            ["python", service],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.processes[service] = proc
        self.restarts.setdefault(service, 0)

    def restart(self, service):

        self.restarts[service] += 1

        if self.restarts[service] > 3:
            log(f"🧊 BLOCKED → {service}")
            return

        log(f"🔁 RESTART → {service}")
        self.start(service)

    def monitor(self):

        while True:
            time.sleep(2)

            for service, proc in list(self.processes.items()):

                state = self.bus.check(service)

                # ❌ process died
                if proc.poll() is not None:
                    log(f"💀 DEAD → {service}")
                    self.restart(service)
                    continue

                # ⚠️ heartbeat missing
                if state == "STALE":
                    log(f"⚠️ STALE → {service}")
                    self.restart(service)

                elif state == "ACTIVE":
                    log(f"❤️ ACTIVE → {service}")

# ----------------------------
# SYSTEMD CORE
# ----------------------------
class OmegaSystemD4:

    def __init__(self, services):
        self.services = services
        self.bus = HeartbeatBus()
        self.runtime = ServiceRuntime(self.bus)

    def boot(self):

        log("🧠 BOOT START")

        self.bus.start()

        for s in self.services:
            self.runtime.start(s)

        log("🟢 BOOT COMPLETE")

        self.runtime.monitor()

# ----------------------------
# ENTRY
# ----------------------------
if __name__ == "__main__":

    services = [f for f in os.listdir(".") if f.endswith(".py")]
    OmegaSystemD4(services).boot()
