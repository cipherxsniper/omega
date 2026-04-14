import os
import time
import json
import random
import requests
import importlib.util
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
OMEGA_DIR = os.path.expanduser("~/Omega")
MEMORY_FILE = "omega_v27_memory.json"
MODEL_FILE = "omega_v27_shared_model.json"

# -----------------------------
# 🌐 INTERNET INGESTION LAYER (v27)
# -----------------------------
class InternetIngestionV27:
    def fetch_crypto(self):
        try:
            r = requests.get(
                "https://api.coindesk.com/v1/bpi/currentprice.json",
                timeout=3
            )
            return r.json()["bpi"]["USD"]["rate_float"]
        except:
            return random.random() * 100

    def fetch_news_signal(self):
        try:
            r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=3)
            return len(r.text) % 100
        except:
            return random.random() * 10

    def fetch_all(self):
        return [
            self.fetch_crypto() % 100,
            self.fetch_news_signal(),
            random.random()
        ]


# -----------------------------
# 🧠 SHARED SWARM MODEL (v26 carried forward)
# -----------------------------
class SharedSwarmModelV27:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random())
        self.lr = 0.02

    def predict(self, brain, features):
        score = self.weights[brain]
        for f in features:
            score += self.weights[str(f)] * 0.01
        return score

    def train(self, brain, features, reward):
        error = reward - self.weights[brain]
        self.weights[brain] += self.lr * error

        for f in features:
            self.weights[str(f)] += self.lr * error * 0.005

    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump(dict(self.weights), f, indent=2)


# -----------------------------
# 🧠 DYNAMIC BRAIN LOADER (AUTO IMPORT ALL FILES)
# -----------------------------
class BrainRegistryV27:
    def __init__(self):
        self.brains = {}

    def discover_brains(self):
        files = [
            f for f in os.listdir(OMEGA_DIR)
            if f.endswith(".py") and "omega_" not in f
        ]

        # include explicit brains too
        explicit = [
            "Brain_00_v10.py",
            "Brain_11_v10.py",
            "Brain_22_v10.py",
            "brain_01.py",
            "brain_02.py",
            "wink_brain.py",
            "ParallelBrain.py",
            "iot_brain.py"
        ]

        all_files = set(files + explicit)

        return list(all_files)

    def load_brain(self, file):
        path = os.path.join(OMEGA_DIR, file)

        if not os.path.exists(path):
            return None

        spec = importlib.util.spec_from_file_location(file[:-3], path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module


# -----------------------------
# 💾 SWARM MEMORY BUS
# -----------------------------
class MemoryBusV27:
    def __init__(self):
        self.memory = defaultdict(list)

    def write(self, brain, data):
        self.memory[brain].append({
            "t": time.time(),
            "data": data
        })

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)


# -----------------------------
# 🌐 OMEGA v27 SWARM INTERNET MESH
# -----------------------------
class OmegaSwarmV27:
    def __init__(self):
        self.net = InternetIngestionV27()
        self.model = SharedSwarmModelV27()
        self.registry = BrainRegistryV27()
        self.memory = MemoryBusV27()

        self.step = 0
        self.running = True

        self.brain_files = self.registry.discover_brains()
        print(f"[v27] Registered brains: {len(self.brain_files)}")

    def decision(self, score):
        return "optimize" if score > 0.5 else "explore"

    def run(self):
        print("[v27] OMEGA INTERNET SWARM MESH ONLINE")

        while self.running:
            self.step += 1

            features = self.net.fetch_all()

            for brain_file in self.brain_files:
                brain_name = brain_file.replace(".py", "")

                score = self.model.predict(brain_name, features)

                # REAL WORLD SIGNAL BASED TARGET
                target = 1.0 if features[0] > 50 else 0.0

                self.model.train(brain_name, features, target)

                decision = self.decision(score)

                self.memory.write(brain_name, {
                    "step": self.step,
                    "features": features,
                    "score": score,
                    "decision": decision,
                    "source": "internet_ingestion_v27"
                })

                print(f"[v27] {brain_name} → {decision} | score={score:.3f}")

            if self.step % 10 == 0:
                self.model.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV27().run()
