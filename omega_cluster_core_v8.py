import os
import sys
import time
import json
import random
import subprocess
import threading
from collections import defaultdict

from omega_ml_core_v8 import OmegaMLCoreV8

# ---------------------------
# CONFIG
# ---------------------------
BRAIN_FILES = [
    "Brain_00_v10.py",
    "Brain_11_v10.py",
    "Brain_22_v10.py",
    "brain_01.py",
    "brain_02.py",
    "wink_brain.py",
]

LOG_FILE = "omega_cluster.log"
MEMORY_FILE = "omega_cluster_memory.json"
BROADCAST_FILE = "omega_broadcast.json"

# ---------------------------
# CORE SYSTEM
# ---------------------------
class OmegaClusterCoreV8:
    def __init__(self):
        self.processes = {}
        self.memory = defaultdict(list)
        self.running = True

        # 🧠 ML CORE
        self.ml = OmegaMLCoreV8()

        # ⚡ system intelligence state
        self.global_state = {
            "mode": "adaptive",
            "last_top_brain": None,
            "cycle": 0
        }

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[CLUSTER V8] {time.strftime('%H:%M:%S')} {msg}"
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

        if len(self.memory[brain]) > 100:
            self.memory[brain] = self.memory[brain][-100:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    # ---------------------------
    # GLOBAL BROADCAST
    # ---------------------------
    def broadcast(self, payload):
        with open(BROADCAST_FILE, "w") as f:
            json.dump(payload, f, indent=2)

    # ---------------------------
    # PROCESS OUTPUT CAPTURE
    # ---------------------------
    def capture_output(self, brain, proc):
        for line in proc.stdout:
            try:
                data = json.loads(line.strip())
                self.write_memory(brain, data)
            except:
                self.write_memory(brain, {"raw": line.strip()})

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
            text=True,
            bufsize=1
        )

        self.processes[brain_file] = proc

        threading.Thread(
            target=self.capture_output,
            args=(brain_file, proc),
            daemon=True
        ).start()

        self.log(f"Started {brain_file}")

    # ---------------------------
    # MONITOR (SELF-HEAL)
    # ---------------------------
    def monitor(self):
        while self.running:
            for brain, proc in list(self.processes.items()):
                if proc.poll() is not None:
                    self.log(f"{brain} crashed → restarting")
                    self.start_brain(brain)

            time.sleep(2)

    # ---------------------------
    # 🧠 LEARNING LOOP (ML CORE)
    # ---------------------------
    def learning_loop(self):
        while self.running:
            try:
                self.global_state["cycle"] += 1

                top_brain = None
                top_score = -1

                for brain in list(self.memory.keys()):
                    mem = self.memory[brain]

                    decision, features = self.ml.decide(brain, mem)

                    # ⚡ ACTION GENERATION
                    if decision == "explore":
                        action = {"action": "random_explore"}
                    else:
                        action = {"action": "optimize"}

                    self.write_memory(brain, action)

                    # ⚡ REWARD BASED ON ACTIVITY
                    reward = random.uniform(0.1, 1.0) + len(mem) * 0.001
                    self.ml.reward(brain, reward)

                    # ⚡ TRAIN MODEL
                    self.ml.train(features, decision)

                    if reward > top_score:
                        top_score = reward
                        top_brain = brain

                self.global_state["last_top_brain"] = top_brain

                # 🌐 BROADCAST GLOBAL STATE
                self.broadcast({
                    "cycle": self.global_state["cycle"],
                    "top_brain": top_brain,
                    "mode": self.global_state["mode"]
                })

                self.ml.save_model()

                self.log(f"ML Cycle {self.global_state['cycle']} | TOP: {top_brain}")

            except Exception as e:
                self.log(f"ML ERROR: {e}")

            time.sleep(3)

    # ---------------------------
    # 🧬 AUTO BRAIN UPGRADE SYSTEM
    # ---------------------------
    def auto_upgrade_brains(self):
        template = '''
import time
import json
import random

MEMORY_FILE = "omega_cluster_memory.json"
BROADCAST_FILE = "omega_broadcast.json"

def read_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def emit(data):
    print(json.dumps(data), flush=True)

while True:
    memory = read_json(MEMORY_FILE)
    broadcast = read_json(BROADCAST_FILE)

    my_name = __file__
    my_mem = memory.get(my_name, [])

    signal = random.random()
    mode = broadcast.get("mode", "adaptive")

    if mode == "adaptive":
        action = "optimize" if signal > 0.4 else "explore"
    else:
        action = "explore"

    output = {
        "brain": my_name,
        "signal": signal,
        "action": action,
        "memory_size": len(my_mem),
        "cycle": broadcast.get("cycle", 0)
    }

    emit(output)

    time.sleep(2)
'''

        for brain in BRAIN_FILES:
            try:
                with open(brain, "w") as f:
                    f.write(template)
                self.log(f"Upgraded {brain}")
            except Exception as e:
                self.log(f"Upgrade failed {brain}: {e}")

    # ---------------------------
    # LAUNCH SYSTEM
    # ---------------------------
    def launch(self):
        self.log("🚀 OMEGA V8 CLUSTER BOOTING")

        # 🧬 upgrade brains automatically
        self.auto_upgrade_brains()

        # 🧠 start brains
        for b in BRAIN_FILES:
            self.start_brain(b)

        # 🛡 monitor thread
        threading.Thread(target=self.monitor, daemon=True).start()

        # 🧠 ML thread
        threading.Thread(target=self.learning_loop, daemon=True).start()

        self.log("⚡ CLUSTER ACTIVE (ML ENABLED)")

        while True:
            time.sleep(1)


# ---------------------------
# ENTRY
# ---------------------------
if __name__ == "__main__":
    OmegaClusterCoreV8().launch()
