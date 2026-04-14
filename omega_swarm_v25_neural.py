import os
import json
import time
import random
import numpy as np
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MODEL_FILE = "omega_v25_neural_model.json"
MEMORY_FILE = "omega_v25_memory.json"

# -----------------------------
# 🧠 SIMPLE NEURAL NETWORK CORE
# -----------------------------
class NeuralCoreV25:
    def __init__(self, input_size=3, hidden=8, lr=0.01):
        self.lr = lr

        # weights
        self.W1 = np.random.randn(input_size, hidden) * 0.1
        self.B1 = np.zeros((hidden,))
        self.W2 = np.random.randn(hidden, 1) * 0.1
        self.B2 = np.zeros((1,))

        self.load()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, x):
        self.z1 = np.dot(x, self.W1) + self.B1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.B2
        self.out = self.sigmoid(self.z2)
        return self.out

    def train(self, x, y):
        y_hat = self.forward(x)

        error = y_hat - y
        d_out = error * y_hat * (1 - y_hat)

        dW2 = np.dot(self.a1.reshape(-1,1), d_out)
        dB2 = d_out

        d_hidden = np.dot(self.W2, d_out) * (1 - self.a1**2)

        dW1 = np.outer(x, d_hidden)
        dB1 = d_hidden

        # update
        self.W2 -= self.lr * dW2
        self.B2 -= self.lr * dB2
        self.W1 -= self.lr * dW1
        self.B1 -= self.lr * dB1

    def predict(self, x):
        return self.forward(x)

    def save(self):
        data = {
            "W1": self.W1.tolist(),
            "W2": self.W2.tolist(),
            "B1": self.B1.tolist(),
            "B2": self.B2.tolist()
        }
        with open(MODEL_FILE, "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists(MODEL_FILE):
            try:
                with open(MODEL_FILE, "r") as f:
                    d = json.load(f)
                    self.W1 = np.array(d["W1"])
                    self.W2 = np.array(d["W2"])
                    self.B1 = np.array(d["B1"])
                    self.B2 = np.array(d["B2"])
            except:
                pass


# -----------------------------
# 🧠 SWARM MEMORY
# -----------------------------
class MemoryV25:
    def __init__(self):
        self.data = defaultdict(list)

    def store(self, brain, entry):
        self.data[brain].append(entry)

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.data, f, indent=2)


# -----------------------------
# 🧠 SWARM CORE v25
# -----------------------------
class OmegaSwarmV25:
    def __init__(self):
        self.net = NeuralCoreV25()
        self.memory = MemoryV25()
        self.step = 0

    def log(self, msg):
        print(f"[v25] {time.strftime('%H:%M:%S')} {msg}")

    def features(self):
        # REAL structured input (not noise-only anymore)
        return np.array([
            random.random() * 100,
            random.randint(1, 50),
            random.random()
        ])

    def decision(self, output):
        return "optimize" if output > 0.5 else "explore"

    # -----------------------------
    # MAIN LOOP (REAL LEARNING)
    # -----------------------------
    def run(self):
        self.log("OMEGA SWARM v25 NEURAL CORE ONLINE")

        while True:
            self.step += 1
            x = self.features()

            for brain in BRAINS:
                pred = float(self.net.predict(x))

                # structured label (NOT random reward)
                # pattern: higher feature sum => "optimize"
                target = 1.0 if x.sum() > 70 else 0.0

                self.net.train(x, target)

                decision = self.decision(pred)

                self.memory.store(brain, {
                    "step": self.step,
                    "features": x.tolist(),
                    "prediction": pred,
                    "target": target,
                    "decision": decision
                })

                self.log(f"{brain} → {decision} | pred={pred:.3f}")

            if self.step % 10 == 0:
                self.net.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV25().run()
