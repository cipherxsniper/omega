import os
import time
import json
import random
import threading
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MODEL_FILE = "omega_shared_nn.json"
MEMORY_FILE = "omega_shared_memory_v16.json"

LEARNING_RATE = 0.05


# -----------------------------
# 🧠 SHARED NEURAL MATRIX
# -----------------------------
class SharedNeuralMatrix:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random() * 0.01)
        self.lock = threading.Lock()
        self.load()

    # -------------------------
    # PREDICTION
    # -------------------------
    def predict(self, brain, features):
        score = self.weights[brain]

        for f in features:
            score += self.weights[str(f)] * 0.1

        return score

    # -------------------------
    # TRAIN GLOBAL MODEL
    # -------------------------
    def train(self, brain, features, reward):
        with self.lock:
            error = reward - self.weights[brain]

            # update brain weight
            self.weights[brain] += LEARNING_RATE * error

            # update feature weights
            for f in features:
                key = str(f)
                self.weights[key] += LEARNING_RATE * error * 0.01

    # -------------------------
    # SAVE MODEL
    # -------------------------
    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump(dict(self.weights), f, indent=2)

    # -------------------------
    # LOAD MODEL
    # -------------------------
    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)

                for k, v in data.items():
                    self.weights[k] = v

                print("[V16] Shared neural matrix loaded")
            except:
                print("[V16] Model load failed → starting fresh")


# -----------------------------
# 🧠 SWARM MEMORY COLLECTOR
# -----------------------------
class SwarmMemory:
    def __init__(self):
        self.data = defaultdict(list)

    def store(self, brain, features, reward):
        self.data[brain].append({
            "t": time.time(),
            "features": features,
            "reward": reward
        })

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)


# -----------------------------
# 🧠 FEATURE ENGINE
# -----------------------------
def generate_features():
    return [
        random.random(),
        random.randint(1, 100),
        random.random() * 10
    ]


# -----------------------------
# 🧠 V16 ORCHESTRATOR
# -----------------------------
class OmegaSharedNeuralMatrixV16:
    def __init__(self):
        self.model = SharedNeuralMatrix()
        self.memory = SwarmMemory()
        self.running = True
        self.step = 0

    def log(self, msg):
        print(f"[V16] {time.strftime('%H:%M:%S')} {msg}")

    # -------------------------
    # BRAIN SIMULATION LOOP
    # -------------------------
    def brain_cycle(self, brain):
        features = generate_features()

        score = self.model.predict(brain, features)

        decision = "optimize" if score > 0.5 else "explore"
        reward = random.random()

        self.model.train(brain, features, reward)
        self.memory.store(brain, features, reward)

        return brain, decision, reward

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("SHARED NEURAL MATRIX V16 ONLINE")

        while self.running:
            self.step += 1

            results = []

            for brain in BRAINS:
                results.append(self.brain_cycle(brain))

            # periodic save
            if self.step % 5 == 0:
                self.model.save()
                self.memory.save()

            # swarm summary
            opt = sum(1 for r in results if r[1] == "optimize")
            exp = len(results) - opt

            self.log(f"STEP {self.step} | OPT={opt} EXP={exp}")

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSharedNeuralMatrixV16().run()
