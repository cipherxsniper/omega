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

MEMORY_FILE = "omega_v24_memory.json"
MODEL_FILE = "omega_v24_model.json"

# -----------------------------
# 🧠 PERSISTENT SWARM MODEL
# -----------------------------
class PersistentSwarmModelV24:
    def __init__(self):
        self.weights = defaultdict(lambda: 0.5)
        self.lr = 0.05
        self.load()

    def predict(self, brain, features):
        base = self.weights[brain]

        signal = 0.0
        for f in features:
            signal += self.weights[str(round(f, 2))] * 0.01

        return base + signal

    def train(self, brain, features, reward):
        error = reward - self.weights[brain]

        self.weights[brain] += self.lr * error

        for f in features:
            key = str(round(f, 2))
            self.weights[key] += self.lr * error * 0.01

    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump(dict(self.weights), f, indent=2)

    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    data = json.load(f)
                    self.weights.update(data)
            except:
                pass


# -----------------------------
# 💾 PERSISTENT MEMORY LAYER
# -----------------------------
class PersistentMemoryV24:
    def __init__(self):
        self.memory = defaultdict(list)
        self.load()

    def write(self, brain, data):
        self.memory[brain].append({
            "t": time.time(),
            "data": data
        })

        self.save()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    self.memory.update(data)
            except:
                pass

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)


# -----------------------------
# 🧬 CROSS-BRAIN INFLUENCE MATRIX
# -----------------------------
class InfluenceMatrixV24:
    def __init__(self):
        self.matrix = {
            b: {b2: random.uniform(0.8, 1.2) for b2 in BRAINS}
            for b in BRAINS
        }

    def influence(self, brain, value):
        total = 0
        for b in BRAINS:
            total += value * self.matrix[brain][b]
        return total / len(BRAINS)


# -----------------------------
# 🧠 SWARM CORE V24
# -----------------------------
class OmegaSwarmV24:
    def __init__(self):
        self.model = PersistentSwarmModelV24()
        self.memory = PersistentMemoryV24()
        self.influence = InfluenceMatrixV24()

        self.running = True
        self.step = 0

    def log(self, msg):
        print(f"[V24] {time.strftime('%H:%M:%S')} {msg}")

    def decide(self, brain, features):
        score = self.model.predict(brain, features)
        score = self.influence.influence(brain, score)

        return "optimize" if score > 0.5 else "explore"

    # -----------------------------
    # 🧠 MAIN LEARNING LOOP
    # -----------------------------
    def loop(self):
        self.log("OMEGA SWARM v24 PERSISTENT ONLINE")

        while self.running:
            self.step += 1

            features = [
                random.random() * 100,
                random.randint(1, 50),
                random.random()
            ]

            for brain in BRAINS:
                decision = self.decide(brain, features)
                reward = random.random()

                # TRAIN MODEL
                self.model.train(brain, features, reward)

                # STORE MEMORY
                self.memory.write(brain, {
                    "step": self.step,
                    "decision": decision,
                    "reward": reward,
                    "features": features
                })

                self.log(f"{brain} → {decision} | {reward:.4f}")

            # SAVE STATE (PERSISTENCE)
            if self.step % 5 == 0:
                self.model.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV24().loop()
