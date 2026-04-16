import os
import time
import json
import random
import threading
import requests
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

MEMORY_FILE = "omega_v16_memory.json"
LOG_FILE = "omega_v16.log"

# -----------------------------
# SIMPLE NEURAL CORE (v17)
# -----------------------------
class SimpleNeuralCore:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random())
        self.lr = 0.05

    def predict(self, brain, features):
        score = self.weights[brain]
        for f in features:
            score += self.weights.get(f, 0.1) * 0.01
        return score

    def train(self, brain, features, reward):
        error = reward - self.weights[brain]
        self.weights[brain] += self.lr * error

        for f in features:
            self.weights[f] += self.lr * error * 0.01

    def save(self):
        with open("omega_v16_model.json", "w") as f:
            json.dump(dict(self.weights), f, indent=2)


# -----------------------------
# OMEGA MESH CORE v16
# -----------------------------
class OmegaMeshV16:
    def __init__(self):
        self.memory = defaultdict(list)
        self.running = True
        self.ml = SimpleNeuralCore()
        self.step = 0

    # -------------------------
    # LOGGING
    # -------------------------
    def log(self, msg):
        line = f"[v16] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    # -------------------------
    # MEMORY SYSTEM (v18 core)
    # -------------------------
    def store(self, brain, data):
        self.memory[brain].append({
            "t": time.time(),
            "data": data
        })

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    # -------------------------
    # INTERNET INGESTION (v18)
    # -------------------------
    def fetch_live_signal(self):
        try:
            # lightweight public endpoint
            r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=3)
            price = r.json()["bpi"]["USD"]["rate_float"]
            return [price % 1000, price % 100]
        except:
            return [random.random(), random.random()]

    # -------------------------
    # DECISION ENGINE
    # -------------------------
    def decide(self, brain, features):
        score = self.ml.predict(brain, features)

        if score > 0.5:
            return "optimize", features
        else:
            return "explore", features

    # -------------------------
    # SELF MODIFICATION (v19 SAFE)
    # -------------------------
    def self_modify(self):
        try:
            patch = {
                "timestamp": time.time(),
                "mutation": random.choice(["tune_lr", "adjust_memory", "boost_exploration"])
            }

            with open("omega_v16_patch.json", "w") as f:
                json.dump(patch, f, indent=2)

        except Exception as e:
            self.log(f"self_modify error: {e}")

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def run(self):
        self.log("OMEGA v16 MULTI-BRAIN MESH ONLINE")

        while self.running:
            self.step += 1

            live_features = self.fetch_live_signal()

            for brain in BRAINS:
                decision, features = self.decide(brain, live_features)

                reward = random.random()

                self.ml.train(brain, features, reward)

                self.store(brain, {
                    "step": self.step,
                    "decision": decision,
                    "reward": reward,
                    "features": features
                })

                self.log(f"{brain} → {decision} | {reward:.4f}")

            # evolve model occasionally
            if self.step % 5 == 0:
                self.self_modify()
                self.ml.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaMeshV16().run()
