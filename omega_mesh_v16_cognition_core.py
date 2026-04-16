import time
import math
import random
from collections import defaultdict

# =========================
# 🌐 OMEGA V16 COGNITION MESH CORE
# =========================

class Node:
    def __init__(self, concept):
        self.concept = concept
        self.weight = random.uniform(0.2, 1.0)
        self.age = 0
        self.connections = set()
        self.history = []

    def reinforce(self, amount):
        self.weight += amount
        self.weight = min(self.weight, 10.0)
        self.history.append(self.weight)

    def decay(self):
        self.weight *= 0.98
        self.age += 1

    def is_alive(self):
        return self.weight > 0.1


class CognitionMeshV16:
    def __init__(self):
        self.nodes = {}
        self.tick = 0
        self.global_goal = "maximize_coherence_and_knowledge"

    # -------------------------
    # 🌱 INGEST CONCEPTS
    # -------------------------
    def ingest(self, concepts):
        for c in concepts:
            if c not in self.nodes:
                self.nodes[c] = Node(c)
            self.nodes[c].reinforce(0.5)

    # -------------------------
    # 🔗 CONNECT NODES
    # -------------------------
    def connect(self):
        keys = list(self.nodes.keys())
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                a, b = self.nodes[keys[i]], self.nodes[keys[j]]
                if abs(a.weight - b.weight) < 2.5:
                    a.connections.add(b.concept)
                    b.connections.add(a.concept)

    # -------------------------
    # 🧠 SWARM THINKING
    # -------------------------
    def swarm_think(self):
        influence = defaultdict(float)

        for node in self.nodes.values():
            for conn in node.connections:
                influence[conn] += node.weight * 0.1

        for k, v in influence.items():
            if k in self.nodes:
                self.nodes[k].reinforce(v)

    # -------------------------
    # 📉 DECAY SYSTEM
    # -------------------------
    def decay(self):
        for node in self.nodes.values():
            node.decay()

    # -------------------------
    # ❌ PRUNE WEAK NODES
    # -------------------------
    def prune(self):
        to_remove = [k for k, v in self.nodes.items() if not v.is_alive()]
        for k in to_remove:
            del self.nodes[k]

    # -------------------------
    # 📡 SIMULATED INTERNET FEED
    # (hook for your V15 crawler)
    # -------------------------
    def internet_feed(self):
        sample = [
            "artificial intelligence",
            "neural networks",
            "reinforcement learning",
            "emergence",
            "swarm intelligence",
            "utility theory",
            "self organizing systems"
        ]
        return random.sample(sample, 3)

    # -------------------------
    # 🧠 GLOBAL STATE REPORT
    # -------------------------
    def report(self):
        top = sorted(self.nodes.values(), key=lambda x: x.weight, reverse=True)[:10]
        print("\n🧠 V16 MESH STATE")
        print(f"tick={self.tick}, nodes={len(self.nodes)}")
        print("TOP CONCEPTS:")
        for n in top:
            print(f"  {n.concept} → {round(n.weight, 3)}")

    # -------------------------
    # 🔁 MAIN LOOP
    # -------------------------
    def run(self):
        while True:
            self.tick += 1

            # 1. ingest internet concepts
            concepts = self.internet_feed()
            self.ingest(concepts)

            # 2. build connections
            self.connect()

            # 3. swarm cognition step
            self.swarm_think()

            # 4. decay & pruning
            self.decay()
            self.prune()

            # 5. report
            if self.tick % 2 == 0:
                self.report()

            time.sleep(1)


# =========================
# 🚀 START SYSTEM
# =========================

if __name__ == "__main__":
    mesh = CognitionMeshV16()
    mesh.run()
