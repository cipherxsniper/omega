import time
import random
import json
import threading
from collections import defaultdict

LOG_FILE = "omega_cross_brain_v15.log"
MEMORY_FILE = "omega_cross_brain_memory.json"

# ---------------------------
# BRAIN NODE
# ---------------------------
class BrainNode:
    def __init__(self, name):
        self.name = name
        self.state = random.random()
        self.score = 1.0
        self.reputation = 1.0
        self.history = []

    def compute_signal(self, shared_context):
        context_influence = shared_context * 0.5
        noise = random.uniform(-0.05, 0.05)

        decision_bias = sum(self.history[-5:]) / 5 if self.history else 0.5

        decision = "optimize" if decision_bias + context_influence > 0.5 else "explore"

        self.state += noise + (context_influence * 0.1)

        return decision


# ---------------------------
# CROSS-BRAIN NETWORK
# ---------------------------
class CrossBrainNetworkV15:
    def __init__(self):
        self.brains = {
            "brain_00": BrainNode("brain_00"),
            "brain_01": BrainNode("brain_01"),
            "brain_02": BrainNode("brain_02"),
            "wink_brain": BrainNode("wink_brain"),
        }

        self.memory = []
        self.running = True
        self.step = 0

    # ---------------------------
    # LOGGING
    # ---------------------------
    def log(self, msg):
        line = f"[V15] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # MEMORY SHARED LAYER
    # ---------------------------
    def write_memory(self, entry):
        self.memory.append(entry)
        self.memory = self.memory[-500:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    # ---------------------------
    # GLOBAL CONTEXT FIELD
    # ---------------------------
    def compute_global_context(self):
        if not self.memory:
            return 0.5

        return sum(m.get("reward", 0.5) for m in self.memory[-20:]) / 20

    # ---------------------------
    # CROSS-BRAIN UPDATE STEP
    # ---------------------------
    def step_cycle(self):
        self.step += 1

        global_context = self.compute_global_context()

        decisions = {}
        rewards = {}

        # 1. each brain thinks
        for name, brain in self.brains.items():

            decision = brain.compute_signal(global_context)

            reward = random.random()

            # learning
            brain.score = 0.9 * brain.score + 0.1 * reward
            brain.history.append(reward)

            brain.reputation = brain.score + (len(brain.history) * 0.001)

            decisions[name] = decision
            rewards[name] = reward

        # 2. cross-brain influence (neural mesh effect)
        avg_state = sum(b.state for b in self.brains.values()) / len(self.brains)

        for brain in self.brains.values():
            influence = (avg_state - brain.state) * 0.05
            brain.state += influence * brain.reputation

        # 3. global consensus signal
        consensus = max(set(decisions.values()), key=list(decisions.values()).count)

        # 4. store memory event
        self.write_memory({
            "step": self.step,
            "context": global_context,
            "consensus": consensus,
            "decisions": decisions,
            "rewards": rewards
        })

        self.log(f"STEP {self.step} | CONSENSUS: {consensus} | CONTEXT: {global_context:.3f}")

    # ---------------------------
    # MAIN LOOP
    # ---------------------------
    def run(self):
        self.log("OMEGA V15 CROSS-BRAIN NETWORK ONLINE")

        while self.running:
            try:
                self.step_cycle()
                time.sleep(1.2)

            except Exception as e:
                self.log(f"ERROR: {e}")
                time.sleep(2)


# ---------------------------
# START
# ---------------------------
if __name__ == "__main__":
    net = CrossBrainNetworkV15()
    net.run()
