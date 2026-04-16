import os
import time
import json
import socket
import threading
import subprocess
import random
from omega_ml_core_v8 import OmegaMLCoreV8
# ---------------------------
# CONFIG
# ---------------------------
HOST = "127.0.0.1"
PORT = 5555

BRAIN_FILES = [
    "Brain_00_v10.py",
    "Brain_11_v10.py",
    "Brain_22_v10.py",
    "brain_01.py",
    "brain_02.py",
    "ParallelBrain.py",
    "wink_brain.py"
]

STATE_FILE = "omega_v7_state.json"
LOG_FILE = "omega_v7.log"

# ---------------------------
# CLUSTER CORE
# ---------------------------
class OmegaClusterV7:

    def __init__(self):
        self.processes = {}
        self.clients = []
        self.running = True

        # adaptive system params
        self.params = {
            "decay": 0.99,
            "mutation": 0.01,
            "pressure": 1.0
        }

        self.scores = {b: 1.0 for b in BRAIN_FILES}
        self.lock = threading.Lock()

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[V7] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # SOCKET SERVER (REAL IPC)
    # ---------------------------
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(10)

        self.log(f"IPC BUS ACTIVE {HOST}:{PORT}")

        while self.running:
            client, addr = server.accept()
            self.clients.append(client)
            threading.Thread(
                target=self.handle_client,
                args=(client,),
                daemon=True
            ).start()

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(4096)
                if not data:
                    break

                msg = data.decode()

                # broadcast to all brains
                self.broadcast(msg)

                # influence system
                self.process_message(msg)

            except:
                break

        client.close()

    def broadcast(self, msg):
        for c in self.clients:
            try:
                c.sendall(msg.encode())
            except:
                pass

    # ---------------------------
    # MESSAGE PROCESSING
    # ---------------------------
    def process_message(self, msg):
        # simple scoring trigger
        for b in self.scores:
            if b in msg:
                self.scores[b] *= (1 + 0.01)

        self.normalize_scores()

    def normalize_scores(self):
        total = sum(self.scores.values()) or 1
        for k in self.scores:
            self.scores[k] /= total

    # ---------------------------
    # SELF-MODIFICATION ENGINE (v6)
    # ---------------------------
    def self_modify(self):
        while self.running:

            # adaptive mutation
            self.params["decay"] *= random.uniform(0.995, 1.005)
            self.params["mutation"] *= random.uniform(0.99, 1.01)
            self.params["pressure"] *= random.uniform(0.98, 1.02)

            # clamp values
            self.params["decay"] = min(max(self.params["decay"], 0.9), 1.0)
            self.params["mutation"] = min(max(self.params["mutation"], 0.001), 0.1)

            self.log(f"SELF-MODIFY {self.params}")

            self.save_state()

            time.sleep(5)

    # ---------------------------
    # STATE SAVE
    # ---------------------------
    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump({
                "params": self.params,
                "scores": self.scores
            }, f, indent=2)

    # ---------------------------
    # PROCESS MANAGEMENT
    # ---------------------------
    def start_brain(self, brain):
        if not os.path.exists(brain):
            self.log(f"Missing {brain}")
            return

        proc = subprocess.Popen(
            ["python", brain],
        )

        self.processes[brain] = proc
        self.log(f"Started {brain}")

    def monitor(self):
        while self.running:
            for b, p in list(self.processes.items()):
                if p.poll() is not None:
                    self.log(f"{b} crashed → restart")
                    self.start_brain(b)

            time.sleep(3)

    # ---------------------------
    # LAUNCH
    # ---------------------------
    def launch(self):
        self.log("OMEGA V7 SWARM BOOTING")

        for b in BRAIN_FILES:
            self.start_brain(b)

        threading.Thread(target=self.start_server, daemon=True).start()
        threading.Thread(target=self.monitor, daemon=True).start()
        threading.Thread(target=self.self_modify, daemon=True).start()

        self.log("SWARM ONLINE")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    OmegaClusterV7().launch()

# OPTIMIZED BY v29 ENGINE
