import os
import time
import json
import subprocess
import threading
from collections import defaultdict, deque

# ---------------------------
# BRAIN REGISTRY (NOW INCLUDES WINK BRAIN)
# ---------------------------
BRAIN_FILES = [
    "Brain_00_v10.py",
    "Brain_11_v10.py",
    "Brain_22_v10.py",
    "brain_01.py",
    "brain_02.py",
    "ParallelBrain.py",
    "wink_brain.py"
]

LOG_FILE = "omega_cluster.log"
MEMORY_FILE = "omega_cluster_memory.json"
STATE_FILE = "omega_cluster_state.json"


# ---------------------------
# OMEGA CLUSTER CORE
# ---------------------------
class OmegaClusterCore:

    def __init__(self):
        self.processes = {}
        self.running = True

        # shared swarm memory
        self.memory_bus = defaultdict(lambda: deque(maxlen=100))
        self.heartbeats = {}
        self.scores = defaultdict(lambda: 1.0)

        self.lock = threading.Lock()

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[CLUSTER] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # STATE SAVE (FULL SWARM SNAPSHOT)
    # ---------------------------
    def save_state(self):
        state = {
            "time": time.time(),
            "processes": list(self.processes.keys()),
            "scores": dict(self.scores),
            "heartbeats": self.heartbeats
        }

        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    # ---------------------------
    # MEMORY BUS WRITE
    # ---------------------------
    def broadcast(self, brain, data):
        with self.lock:
            self.memory_bus[brain].append({
                "t": time.time(),
                "data": data
            })

    # ---------------------------
    # HEARTBEAT SYSTEM
    # ---------------------------
    def heartbeat(self, brain):
        self.heartbeats[brain] = time.time()

    def check_heartbeats(self):
        while self.running:
            now = time.time()

            for brain in list(self.heartbeats.keys()):
                if now - self.heartbeats[brain] > 10:
                    self.log(f"{brain} unresponsive → restarting")
                    self.restart_brain(brain)

            time.sleep(5)

    # ---------------------------
    # START BRAIN
    # ---------------------------
    def start_brain(self, brain_file):
        if not os.path.exists(brain_file):
            self.log(f"Missing brain: {brain_file}")
            return

        proc = subprocess.Popen(
            ["python", brain_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.processes[brain_file] = proc
        self.heartbeat(brain_file)
        self.log(f"Started {brain_file}")

    # ---------------------------
    # RESTART BRAIN
    # ---------------------------
    def restart_brain(self, brain_file):
        try:
            proc = self.processes.get(brain_file)
            if proc:
                proc.kill()
        except:
            pass

        time.sleep(1)
        self.start_brain(brain_file)

    # ---------------------------
    # MONITOR LOOP
    # ---------------------------
    def monitor(self):
        while self.running:

            for brain, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    self.log(f"{brain} crashed → restart")
                    self.restart_brain(brain)

            self.save_state()
            time.sleep(1.5)

    # ---------------------------
    # SWARM INTELLIGENCE LOOP
    # ---------------------------
    def swarm_loop(self):
        while self.running:

            # simulate cross-brain learning
            for brain in BRAIN_FILES:
                self.scores[brain] *= 0.999 + (len(self.memory_bus[brain]) * 0.0001)

            # normalize
            total = sum(self.scores.values()) or 1
            for k in self.scores:
                self.scores[k] /= total

            time.sleep(3)

    # ---------------------------
    # LAUNCH ALL SYSTEMS
    # ---------------------------
    def launch(self):
        self.log("OMEGA CLUSTER v2 BOOTING")

        for b in BRAIN_FILES:
            self.start_brain(b)

        threading.Thread(target=self.monitor, daemon=True).start()
        threading.Thread(target=self.check_heartbeats, daemon=True).start()
        threading.Thread(target=self.swarm_loop, daemon=True).start()

        self.log("SWARM ACTIVE (Brains + Wink + Parallel Network)")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    OmegaClusterCore().launch()

# OPTIMIZED BY v29 ENGINE
