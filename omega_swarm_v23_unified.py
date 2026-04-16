import os
import time
import json
import random
import socket
import threading
import ast
import requests
from collections import defaultdict

# -----------------------------
# CONFIG
# -----------------------------
BRAINS = ["brain_00", "brain_01", "brain_02", "wink_brain"]

PORT = 5050
HOST = "127.0.0.1"

MEMORY_FILE = "omega_swarm_memory.json"
MODEL_FILE = "omega_swarm_model.json"

# -----------------------------
# 🌐 API INGESTION LAYER (v21)
# -----------------------------
class DataIngestion:
    def fetch_crypto(self):
        try:
            r = requests.get(
                "https://api.coindesk.com/v1/bpi/currentprice.json",
                timeout=3
            )
            price = r.json()["bpi"]["USD"]["rate_float"]
            return price
        except:
            return random.random() * 100

    def fetch_rss(self):
        try:
            r = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=3)
            return len(r.text) % 1000
        except:
            return random.random()

    def fetch_all(self):
        return [
            self.fetch_crypto() % 100,
            self.fetch_rss() % 50,
            random.random()
        ]


# -----------------------------
# 🧠 SWARM NEURAL CONSENSUS (v20)
# -----------------------------
class SwarmModel:
    def __init__(self):
        self.weights = defaultdict(lambda: random.random())
        self.lr = 0.03

    def predict(self, brain, features):
        score = self.weights[brain]

        for f in features:
            score += self.weights[str(f)] * 0.01

        return score

    def train(self, brain, features, reward):
        error = reward - self.weights[brain]

        self.weights[brain] += self.lr * error

        for f in features:
            self.weights[str(f)] += self.lr * error * 0.01

    def save(self):
        with open(MODEL_FILE, "w") as f:
            json.dump(dict(self.weights), f, indent=2)


# -----------------------------
# 🧬 SAFE SELF-REWRITE ENGINE (v22)
# -----------------------------
class SafeCodeRewriter:
    def analyze(self, file_path):
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())

            return [type(node).__name__ for node in ast.walk(tree)]
        except:
            return []

    def suggest_patch(self, file_path):
        analysis = self.analyze(file_path)

        patch = {
            "file": file_path,
            "timestamp": time.time(),
            "analysis": analysis,
            "suggestion": random.choice([
                "optimize_loop_delay",
                "reduce_memory_write_frequency",
                "improve_feature_normalization"
            ])
        }

        patch_file = f"{file_path}.patch.json"

        with open(patch_file, "w") as f:
            json.dump(patch, f, indent=2)

        return patch_file


# -----------------------------
# ⚡ TCP DISTRIBUTED MESH (v23)
# -----------------------------
class SwarmNetwork:
    def __init__(self):
        self.peers = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def broadcast(self, message):
        data = json.dumps(message).encode()
        self.sock.sendto(data, (HOST, PORT))

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))

        while True:
            data, _ = s.recvfrom(4096)
            msg = json.loads(data.decode())
            print("[NETWORK]", msg)


# -----------------------------
# 🧠 OMEGA SWARM CORE
# -----------------------------
class OmegaSwarmV23:
    def __init__(self):
        self.data = DataIngestion()
        self.model = SwarmModel()
        self.rewriter = SafeCodeRewriter()
        self.net = SwarmNetwork()

        self.memory = defaultdict(list)
        self.running = True
        self.step = 0

    def log(self, msg):
        print(f"[v23] {time.strftime('%H:%M:%S')} {msg}")

    def store(self, brain, data):
        self.memory[brain].append(data)

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    # -----------------------------
    # SWARM CONSENSUS DECISION
    # -----------------------------
    def decide(self, brain, features):
        score = self.model.predict(brain, features)

        if score > 0.5:
            return "optimize"
        return "explore"

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):
        self.log("OMEGA SWARM v23 ONLINE")

        threading.Thread(target=self.net.listen, daemon=True).start()

        while self.running:
            self.step += 1

            features = self.data.fetch_all()

            consensus_votes = []

            for brain in BRAINS:
                decision = self.decide(brain, features)
                reward = random.random()

                self.model.train(brain, features, reward)

                self.store(brain, {
                    "step": self.step,
                    "decision": decision,
                    "reward": reward,
                    "features": features
                })

                consensus_votes.append(decision)

            # 🧠 SWARM CONSENSUS
            final = max(set(consensus_votes), key=consensus_votes.count)

            # ⚡ broadcast decision
            self.net.broadcast({
                "step": self.step,
                "consensus": final
            })

            self.log(f"CONSENSUS: {final} | FEATURES: {features}")

            # 🧬 SAFE SELF-REWRITE
            if self.step % 10 == 0:
                self.rewriter.suggest_patch(__file__)
                self.model.save()

            time.sleep(2)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    OmegaSwarmV23().run()
