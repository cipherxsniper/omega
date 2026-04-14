import os
import sys
import time
import json
import subprocess
import threading
from collections import defaultdict

BRAIN_FILES = [
    "Brain_00_v10.py",
    "Brain_11_v10.py",
    "Brain_22_v10.py",
    "brain_01.py",
    "brain_02.py",
]

LOG_FILE = "omega_cluster.log"
MEMORY_FILE = "omega_cluster_memory.json"

class OmegaClusterCore:
    def __init__(self):
        self.processes = {}
        self.memory = defaultdict(list)
        self.running = True

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[CLUSTER] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # MEMORY BUS
    # ---------------------------
    def write_memory(self, brain, data):
        self.memory[brain].append({
            "t": time.time(),
            "data": data
        })

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

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
        self.log(f"Started {brain_file}")

    # ---------------------------
    # MONITOR
    # ---------------------------
    def monitor(self):
        while self.running:
            for brain, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    self.log(f"{brain} crashed → restarting")
                    self.start_brain(brain)

            time.sleep(1.5)

    # ---------------------------
    # LAUNCH ALL BRAINS
    # ---------------------------
    def launch(self):
        self.log("OMEGA CLUSTER BOOTING")

        for b in BRAIN_FILES:
            self.start_brain(b)

        monitor_thread = threading.Thread(target=self.monitor, daemon=True)
        monitor_thread.start()

        self.log("CLUSTER ACTIVE")

        while True:
            time.sleep(1)

if __name__ == "__main__":
    OmegaClusterCore().launch()

# OPTIMIZED BY v29 ENGINE
