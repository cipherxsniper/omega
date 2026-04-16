import time
import random
import json
import threading
import math

LOG_FILE = "omega_cross_brain_v16.log"
MEMORY_FILE = "omega_cross_brain_v16_memory.json"

# ---------------------------
# BRAIN NODE
# ---------------------------
class BrainNode:
    def __init__(self, name):
        self.name = name
        self.state = random.random()
        self.score = 1.0
        self.reputation = 1.0
        self.learning_rate = 0.1
        self.history = []

    def entropy(self):
        return random.uniform(-0.2, 0.2)

    def ingest_signal(self, signal):
        return signal * 0.05

    def think(self, global_signal):
        bias = sum(self.history[-5:]) / 5 if self.history else 0.5

        decision = "optimize" if (bias + global_signal) > 0.5 else "explore"

        # state evolution (ENTROPY LAYER v16)
        self.state += self.entropy()

        return decision


# ---------------------------
# OMEGA NETWORK V16
# ---------------------------
class OmegaCrossBrainV16:
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
    def log(self, msg):
        line = f"[V16] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # ---------------------------
    # v17 LIVE SIGNAL LAYER
    # ---------------------------
    def get_live_signal(self):
        # lightweight "real-world" proxy signal
        return (time.time() % 10) / 10

    # ---------------------------
    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory[-300:], f, indent=2)

    # ---------------------------
    # v18 WEIGHT SHARING LAYER
    # ---------------------------
    def share_weights(self):
        avg_state = sum(b.state for b in self.brains.values()) / len(self.brains)

        for brain in self.brains.values():
            influence = (avg_state - brain.state)

            # strong brains stabilize weak ones
            brain.state += influence * brain.reputation * 0.05

    # ---------------------------
    def step_cycle(self):
        self.step += 1

        global_signal = self.get_live_signal()

        decisions = {}

        # 1. brain processing
        for brain in self.brains.values():

            decision = brain.think(global_signal)

            reward = random.random()

            # learning update
            brain.score = 0.9 * brain.score + 0.1 * reward
            brain.reputation = brain.score + (len(brain.history) * 0.001)

            brain.history.append(reward)

            decisions[brain.name] = decision

        # 2. v18 weight sharing
        self.share_weights()

        # 3. memory storage
        self.memory.append({
            "step": self.step,
            "signal": global_signal,
            "decisions": decisions,
            "avg_state": sum(b.state for b in self.brains.values()) / len(self.brains)
        })

        # 4. log consensus
        consensus = max(set(decisions.values()), key=list(decisions.values()).count)

        self.log(f"STEP {self.step} | CONSENSUS: {consensus} | SIGNAL: {global_signal:.3f}")

        self.save_memory()

    # ---------------------------
    def run(self):
        self.log("OMEGA V16 CROSS-BRAIN + ENTROPY + DATA + WEIGHT SHARING ONLINE")

        while self.running:
            try:
                self.step_cycle()
                time.sleep(1)

            except Exception as e:
                self.log(f"ERROR: {e}")
                time.sleep(2)


# ---------------------------
# START
# ---------------------------
if __name__ == "__main__":
    OmegaCrossBrainV16().run()
