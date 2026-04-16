import os
import time
import json
import socket
import threading
import subprocess
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = [
    "brain_00.py",
    "brain_01.py",
    "brain_02.py",
    "wink_brain.py"
]

STATE_FILE = "omega_mesh_state_v15.json"

HOST = "127.0.0.1"
PORT = 7777

CHECK_INTERVAL = 3


# -----------------------------
# SHARED STATE BUS (v15 CORE)
# -----------------------------
class SharedState:
    def __init__(self):
        self.state = {
            "memory": defaultdict(list),
            "signals": {},
            "consensus": None
        }

    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def write_memory(self, brain, data):
        if brain not in self.state["memory"]:
            self.state["memory"][brain] = []

        self.state["memory"][brain].append({
            "t": time.time(),
            "data": data
        })

        self.save()


# -----------------------------
# 🧠 TCP MESSAGING BUS
# -----------------------------
class MessageBus:
    def __init__(self, state):
        self.state = state

    def start_server(self):
        def handler():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen()

            print("[BUS] Listening on port", PORT)

            while True:
                conn, _ = s.accept()
                data = conn.recv(4096)

                try:
                    msg = json.loads(data.decode())

                    brain = msg.get("brain")
                    payload = msg.get("data")

                    self.state.write_memory(brain, payload)

                    conn.send(b"OK")
                except:
                    conn.send(b"ERROR")

                conn.close()

        threading.Thread(target=handler, daemon=True).start()

    def send(self, brain, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))

            msg = json.dumps({
                "brain": brain,
                "data": data
            }).encode()

            s.send(msg)
            s.close()
        except:
            pass


# -----------------------------
# 🧠 SWARM CONSENSUS ENGINE
# -----------------------------
class ConsensusEngine:
    def decide(self, memory):
        score = 0

        for brain, logs in memory.items():
            score += len(logs) % 10

        if score % 2 == 0:
            return "optimize"
        return "explore"


# -----------------------------
# ⚙️ PROCESS SUPERVISOR
# -----------------------------
class ProcessManager:
    def __init__(self):
        self.procs = {}

    def start(self, brain):
        print(f"[SUPERVISOR] Starting {brain}")

        p = subprocess.Popen(["python", brain])
        self.procs[brain] = p

    def restart(self, brain):
        self.stop(brain)
        self.start(brain)

    def stop(self, brain):
        if brain in self.procs:
            try:
                self.procs[brain].terminate()
            except:
                pass

    def alive(self, brain):
        p = self.procs.get(brain)
        return p and p.poll() is None


# -----------------------------
# 🧬 V15 MESH SUPERVISOR
# -----------------------------
class OmegaMeshSupervisorV15:
    def __init__(self):
        self.state = SharedState()
        self.bus = MessageBus(self.state)
        self.consensus = ConsensusEngine()
        self.pm = ProcessManager()
        self.running = True

    def launch_all(self):
        for b in BRAINS:
            self.pm.start(b)

    def monitor(self):
        while self.running:
            for b in BRAINS:
                if not self.pm.alive(b):
                    print(f"[SUPERVISOR] Restarting {b}")
                    self.pm.restart(b)

            time.sleep(CHECK_INTERVAL)

    def consensus_loop(self):
        while self.running:
            decision = self.consensus.decide(self.state.state["memory"])
            self.state.state["consensus"] = decision
            self.state.save()

            print(f"[CONSENSUS] {decision}")

            time.sleep(2)

    def run(self):
        print("[V15] DISTRIBUTED MESH SUPERVISOR ONLINE")

        self.state.load()
        self.bus.start_server()
        self.launch_all()

        threading.Thread(target=self.monitor, daemon=True).start()
        threading.Thread(target=self.consensus_loop, daemon=True).start()

        while True:
            time.sleep(5)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaMeshSupervisorV15().run()
