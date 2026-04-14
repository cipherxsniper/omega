import os
import time
import json
import random
import numpy as np
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MODEL_FILE = "omega_v26_shared_model.json"
MEMORY_FILE = "omega_v26_shared_memory.json"


# -----------------------------
# 🧠 SHARED NEURAL MESH CORE (ONE BRAIN FOR ALL)
# -----------------------------
class SharedNeuralMeshV26:
    def __init__(self, input_size=3, hidden=12, lr=0.01):
        self.lr = lr

        # ONE shared model (this is the key change)
        self.W1 = np.random.randn(input_size, hidden) * 0.1
        self.B1 = np.zeros(hidden)
        self.W2 = np.random.randn(hidden, 1) * 0.1
        self.B2 = np.zeros(1)

        self.load()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        self.z1 = np.dot(x, self.W1) + self.B1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.B2
        return self.sigmoid(self.z2)

    def train(self, x, y):
        y_hat = self.forward(x)

        error = y_hat - y
        d_out = error * y_hat * (1 - y_hat)

        dW2 = np.dot(self.a1.reshape(-1, 1), d_out)
        dB2 = d_out

        d_hidden = np.dot(self.W2, d_out) * (1 - self.a1 ** 2)

        dW1 = np.outer(x, d_hidden)
        dB1 = d_hidden

        # update shared weights
        self.W1 -= self.lr * dW1
        self.W2 -= self.lr * dW2
        self.B1 -= self.lr * dB1
        self.B2 -= self.lr * dB2

    def predict(self, x):
        return self.forward(x)

    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump({
                "W1": self.W1.tolist(),
                "W2": self.W2.tolist(),
                "B1": self.B1.tolist(),
                "B2": self.B2.tolist()
            }, f)

    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                d = json.load(open(MODEL_FILE))
                self.W1 = np.array(d["W1"])
                self.W2 = np.array(d["W2"])
                self.B1 = np.array(d["B1"])
                self.B2 = np.array(d["B2"])
            except:
                pass


# -----------------------------
# 💾 UNIFIED MEMORY FIELD
# -----------------------------
class UnifiedMemoryV26:
    def __init__(self):
        self.memory = []

    def store(self, entry):
        self.memory.append(entry)

        if len(self.memory) > 2000:
            self.memory = self.memory[-200:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)


# -----------------------------
# 🧠 OMEGA SWARM v26 (TRUE SHARED MIND)
# -----------------------------
class OmegaSwarmV26:
    def __init__(self):
        self.mesh = SharedNeuralMeshV26()
        self.memory = UnifiedMemoryV26()
        self.step = 0

    def log(self, msg):
        print(f"[v26] {time.strftime('%H:%M:%S')} {msg}")

    def features(self):
        # structured environment input
        return np.array([
            random.random() * 100,
            random.randint(1, 50),
            random.random()
        ])

    def decision(self, score):
        return "optimize" if score > 0.5 else "explore"

    # -----------------------------
    # MAIN SWARM LOOP
    # -----------------------------
    def run(self):
        self.log("OMEGA v26 SHARED NEURAL MESH ONLINE")

        while True:
            self.step += 1

            x = self.features()

            # shared prediction (ONE brain)
            prediction = float(self.mesh.predict(x))

            # structured learning rule (pattern-based, not random reward)
            target = 1.0 if x.sum() > 70 else 0.0

            # train shared mesh ONCE per step (all brains contribute)
            self.mesh.train(x, target)

            # ALL brains experience SAME cognition
            for brain in BRAINS:
                decision = self.decision(prediction)

                self.memory.store({
                    "step": self.step,
                    "brain": brain,
                    "features": x.tolist(),
                    "prediction": prediction,
                    "target": target,
                    "decision": decision
                })

                self.log(f"{brain} → {decision} | shared={prediction:.3f}")

            if self.step % 10 == 0:
                self.mesh.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV26().run()
