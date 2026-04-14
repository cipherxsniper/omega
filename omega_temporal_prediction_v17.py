import os
import time
import json
import random
import math
from collections import defaultdict, deque

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MODEL_FILE = "omega_shared_nn_v17.json"
MEMORY_FILE = "omega_temporal_memory_v17.json"

LEARNING_RATE = 0.04
DECAY = 0.92
SEQ_LEN = 5


# -----------------------------
# 🧠 TEMPORAL NEURAL MATRIX
# -----------------------------
class TemporalNeuralMatrix:
    def __init__(self):
        self.w = defaultdict(lambda: random.random() * 0.01)
        self.locked = False
        self.load()

    # -------------------------
    # PREDICT NEXT STATE
    # -------------------------
    def predict(self, brain, sequence):
        score = self.w[brain]

        # temporal weighting (recent > old)
        for i, step in enumerate(sequence):
            weight = DECAY ** (len(sequence) - i)

            for f in step["features"]:
                score += self.w[str(f)] * weight * 0.1

            score += step["reward"] * weight

        return score

    # -------------------------
    # TRAIN FROM SEQUENCE
    # -------------------------
    def train(self, brain, sequence, reward):
        error = reward - self.w[brain]

        self.w[brain] += LEARNING_RATE * error

        # propagate through time steps
        for step in sequence:
            for f in step["features"]:
                key = str(f)
                self.w[key] += LEARNING_RATE * error * 0.01

    # -------------------------
    # SAVE / LOAD
    # -------------------------
    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump(dict(self.w), f, indent=2)

    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                for k, v in data.items():
                    self.w[k] = v

                print("[V17] Temporal model loaded")
            except:
                print("[V17] Starting fresh model")


# -----------------------------
# 🧠 TEMPORAL MEMORY BUFFER
# -----------------------------
class TemporalMemory:
    def __init__(self):
        self.memory = defaultdict(lambda: deque(maxlen=SEQ_LEN))

    def add(self, brain, features, reward):
        self.memory[brain].append({
            "t": time.time(),
            "features": features,
            "reward": reward
        })

    def get_sequence(self, brain):
        return list(self.memory[brain])

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump({k: list(v) for k, v in self.memory.items()}, f, indent=2)


# -----------------------------
# 🧠 FEATURE ENGINE
# -----------------------------
def generate_features():
    return [
        random.random(),
        random.randint(1, 50),
        math.sin(time.time() % 10)
    ]


# -----------------------------
# 🧠 V17 TEMPORAL ORCHESTRATOR
# -----------------------------
class OmegaTemporalV17:
    def __init__(self):
        self.model = TemporalNeuralMatrix()
        self.memory = TemporalMemory()
        self.step = 0
        self.running = True

    def log(self, msg):
        print(f"[V17] {time.strftime('%H:%M:%S')} {msg}")

    # -------------------------
    # SINGLE BRAIN CYCLE
    # -------------------------
    def brain_tick(self, brain):
        features = generate_features()
        reward = random.random()

        self.memory.add(brain, features, reward)

        seq = self.memory.get_sequence(brain)

        prediction = self.model.predict(brain, seq)
        decision = "optimize" if prediction > 0.5 else "explore"

        self.model.train(brain, seq, reward)

        return brain, decision, reward

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("TEMPORAL PREDICTION V17 ONLINE")

        while self.running:
            self.step += 1

            results = []

            for brain in BRAINS:
                results.append(self.brain_tick(brain))

            # periodic save
            if self.step % 5 == 0:
                self.model.save()
                self.memory.save()

            opt = sum(1 for r in results if r[1] == "optimize")
            exp = len(results) - opt

            self.log(f"STEP {self.step} | OPT={opt} EXP={exp}")

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaTemporalV17().run()
