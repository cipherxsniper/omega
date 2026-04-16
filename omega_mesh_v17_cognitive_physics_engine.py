import time
import random
import math
from collections import defaultdict

# =========================================================
# 🧠 OMEGA V17 — COGNITIVE PHYSICS ENGINE
# =========================================================

class Node:
    def __init__(self, concept):
        self.concept = concept
        self.weight = random.uniform(0.5, 2.0)
        self.age = 0
        self.connections = set()

    def decay(self, entropy):
        # entropy increases decay pressure
        self.weight *= (0.985 - entropy * 0.02)
        self.age += 1

    def alive(self):
        return self.weight > 0.15


class CognitivePhysicsV17:
    def __init__(self):
        self.nodes = {}
        self.tick = 0

        # 🧠 global fields
        self.entropy_field = 0.1
        self.goal = "maximize_emergent_intelligence"

    # =====================================================
    # 🌱 INGEST (CORE INPUT LAYER)
    # =====================================================
    def ingest(self, concepts):
        for c in concepts:
            if c not in self.nodes:
                self.nodes[c] = Node(c)
            self.nodes[c].weight += 0.6

    # =====================================================
    # 🔗 CONNECTION FIELD (GRAPH FORMATION)
    # =====================================================
    def connect(self):
        keys = list(self.nodes.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a = self.nodes[keys[i]]
                b = self.nodes[keys[j]]

                similarity = 1 / (1 + abs(a.weight - b.weight))

                if similarity > 0.55:
                    a.connections.add(b.concept)
                    b.connections.add(a.concept)

    # =====================================================
    # ⚖️ COMPETITIVE PHYSICS (KEY V17 FEATURE)
    # =====================================================
    def competition(self):
        weights = {k: v.weight for k, v in self.nodes.items()}

        total = sum(weights.values()) + 1e-6

        for node in self.nodes.values():
            share = node.weight / total

            # winners grow, losers decay faster
            if share > 0.12:
                node.weight *= 1.04
            elif share < 0.05:
                node.weight *= 0.93

    # =====================================================
    # 🧬 ENTROPY FIELD (ANTI-COLLAPSE SYSTEM)
    # =====================================================
    def update_entropy(self):
        if len(self.nodes) == 0:
            self.entropy_field = 0.0
            return

        weights = [n.weight for n in self.nodes.values()]
        avg = sum(weights) / len(weights)

        variance = sum((w - avg) ** 2 for w in weights) / len(weights)
        self.entropy_field = min(1.0, variance / (avg + 1e-6))

    # =====================================================
    # 🧠 SWARM INFLUENCE PROPAGATION
    # =====================================================
    def propagate(self):
        influence = defaultdict(float)

        for node in self.nodes.values():
            for conn in node.connections:
                if conn in self.nodes:
                    influence[conn] += node.weight * 0.08

        for k, v in influence.items():
            self.nodes[k].weight += v

    # =====================================================
    # 📉 DECAY SYSTEM (ENTROPY-AWARE)
    # =====================================================
    def decay(self):
        for node in self.nodes.values():
            node.decay(self.entropy_field)

    # =====================================================
    # ❌ PRUNING SYSTEM
    # =====================================================
    def prune(self):
        dead = [k for k, v in self.nodes.items() if not v.alive()]
        for k in dead:
            del self.nodes[k]

    # =====================================================
    # 🌐 OPTIONAL BLOCK A — INTERNET COGNITION HOOK
    # =====================================================
    def internet_feed(self):
        # Replace this with real scraper / API later
        return [
            "artificial intelligence",
            "reinforcement learning",
            "emergence",
            "swarm intelligence",
            "utility theory",
            "self organizing systems",
            "deep learning"
        ]

    # =====================================================
    # 🔥 OPTIONAL BLOCK B — SELF-REWRITE HOOK (DISABLED SAFELY)
    # =====================================================
    def self_rewrite_hook(self):
        # future V18+ system mutation layer
        # currently passive safety placeholder
        pass

    # =====================================================
    # 🧬 OPTIONAL BLOCK C — GOAL FIELD INFLUENCE
    # =====================================================
    def apply_goal_pressure(self):
        for node in self.nodes.values():
            if "intelligence" in node.concept:
                node.weight *= 1.01

    # =====================================================
    # 🧠 REPORTING
    # =====================================================
    def report(self):
        top = sorted(self.nodes.values(), key=lambda n: n.weight, reverse=True)[:10]

        print("\n🧠 V17 COGNITIVE PHYSICS STATE")
        print(f"tick={self.tick} | nodes={len(self.nodes)} | entropy={round(self.entropy_field, 4)}")
        print("TOP CONCEPTS:")

        for n in top:
            print(f"  {n.concept} → {round(n.weight, 3)}")

    # =====================================================
    # 🔁 MAIN LOOP (CONTINUOUS COGNITION)
    # =====================================================
    def run(self):
        while True:
            self.tick += 1

            # 1. ingest knowledge
            concepts = self.internet_feed()
            self.ingest(concepts)

            # 2. structure formation
            self.connect()

            # 3. physics of cognition
            self.update_entropy()
            self.propagate()
            self.competition()
            self.apply_goal_pressure()

            # 4. decay + pruning
            self.decay()
            self.prune()

            # 5. optional rewrite hook
            self.self_rewrite_hook()

            # 6. output
            if self.tick % 2 == 0:
                self.report()

            time.sleep(1)


# =========================================================
# 🚀 START
# =========================================================

if __name__ == "__main__":
    engine = CognitivePhysicsV17()
    engine.run()
