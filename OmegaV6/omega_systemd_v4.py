import os
import json
import time
import socket
import threading
import subprocess

HOST = "127.0.0.1"
PORT = 5050

LOG_PREFIX = "[OMEGA V4]"

# ---------------------------
# JOURNAL
# ---------------------------

def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {LOG_PREFIX} {msg}")

# ---------------------------
# SOCKET BUS (KERNEL IPC)
# ---------------------------

class SocketBus:
    def __init__(self):
        self.clients = {}
        self.last_beat = {}

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        log("Socket bus listening...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                msg = json.loads(data)
                service = msg.get("service")
                msg_type = msg.get("type")

                if msg_type == "heartbeat":
                    self.last_beat[service] = time.time()
                    log(f"HEARTBEAT ← {service}")

        except Exception:
            pass
        finally:
            conn.close()

# ---------------------------
# SERVICE AGENT WRAPPER
# ---------------------------

def launch_service_agent(service_file):
    """
    Wraps a service so it MUST emit heartbeats
    """
    return subprocess.Popen(
        ["python", "omega_service_agent_v4.py", service_file]
    )

# ---------------------------
# SERVICE AGENT (runs inside each service)
# ---------------------------

AGENT_CODE = """
import socket, json, time, sys

HOST = "127.0.0.1"
PORT = 5050

service = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

while True:
    msg = json.dumps({
        "service": service,
        "type": "heartbeat",
        "ts": time.time()
    })

    sock.send(msg.encode())
    time.sleep(2)
"""

# ---------------------------
# KERNEL v4
# ---------------------------

class OmegaSystemD4:

    def __init__(self, manifest):
        self.manifest = manifest
        self.processes = {}
        self.bus = SocketBus()

    def boot(self):
        log("BOOT START")

        # start IPC bus
        threading.Thread(target=self.bus.start_server, daemon=True).start()

        time.sleep(1)

        services = self.manifest.get("services", [])

        for s in services:
            self.start(s)

        log("BOOT COMPLETE")

        self.monitor()

    def start(self, service):
        log(f"START → {service}")

        proc = launch_service_agent(service)

        self.processes[service] = {
            "proc": proc,
            "state": "ACTIVE"
        }

    def monitor(self):
        while True:
            time.sleep(3)

            now = time.time()

            for service in list(self.processes.keys()):

                last = self.bus.last_beat.get(service)

                if not last:
                    log(f"DEGRADED (no heartbeat): {service}")
                    continue

                if now - last > 6:
                    log(f"FAILED (heartbeat timeout): {service}")

                    proc = self.processes[service]["proc"]
                    proc.terminate()

                    log(f"RESTARTING: {service}")
                    self.start(service)

# ---------------------------
# MAIN
# ---------------------------

if __name__ == "__main__":

    if not os.path.exists("omega_manifest.json"):
        print("Missing manifest")
        exit(1)

    manifest = json.load(open("omega_manifest.json"))

    kernel = OmegaSystemD4(manifest)
    kernel.boot()
