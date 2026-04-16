import math
import random
from collections import defaultdict

# -----------------------------
# 🧠 LOCAL NODE BRAIN (V11 CORE)
# -----------------------------
class NodeBrain:

    def __init__(self, brain_id):
        self.id = brain_id
        self.nodes = defaultdict(lambda: {"activation": 1.0, "links": defaultdict(float)})
        self.tick = 0

    def ingest(self, text):
        self.tick += 1
        words = text.lower().split()

        for w in words:
            self.nodes[w]["activation"] += 1.0

        for i in range(len(words) - 1):
            a, b = words[i], words[i+1]
            self.nodes[a]["links"][b] += 1.0
            self.nodes[b]["links"][a] += 1.0

        self._decay()

    def _decay(self):
        for n in self.nodes:
            self.nodes[n]["activation"] *= 0.98

    def top_concepts(self, k=5):
        ranked = sorted(self.nodes.items(), key=lambda x: x[1]["activation"], reverse=True)
        return [(k, v["activation"]) for k, v in ranked[:k]]


# -----------------------------
# 🌐 SWARM COGNITION NETWORK
# -----------------------------
class OmegaSwarmV12:

    def __init__(self, brain_count=5):
        self.brains = [NodeBrain(i) for i in range(brain_count)]

        # shared global belief field
        self.global_beliefs = defaultdict(float)

        self.tick = 0

    # -----------------------------
    # 🧠 BROADCAST INPUT TO SWARM
    # -----------------------------
    def ingest(self, text):
        self.tick += 1

        # each brain processes independently
        for brain in self.brains:
            brain.ingest(text)

        # update global belief field
        self._sync_beliefs()

    # -----------------------------
    # 🌐 SWARM CONSENSUS MECHANISM
    # -----------------------------
    def _sync_beliefs(self):
        aggregate = defaultdict(list)

        # collect all brain outputs
        for brain in self.brains:
            for node, data in brain.nodes.items():
                aggregate[node].append(data["activation"])

        # compute consensus (mean + stability weighting)
        for node, values in aggregate.items():
            mean = sum(values) / len(values)
            stability = 1.0 / (1.0 + math.var(values) if len(values) > 1 else 1.0)

            self.global_beliefs[node] = mean * stability

    # -----------------------------
    # 🧠 SWARM THINKING
    # -----------------------------
    def swarm_state(self):
        ranked = sorted(
            self.global_beliefs.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:10]

    # -----------------------------
    # 🔥 CROSS-BRAIN CONSENSUS SCORE
    # -----------------------------
    def consensus_strength(self):
        if not self.global_beliefs:
            return 0

        vals = list(self.global_beliefs.values())
        return sum(vals) / (len(vals) + 1e-9)


# -----------------------------
# 🚀 DEMO RUN
# -----------------------------
if __name__ == "__main__":
    swarm = OmegaSwarmV12(brain_count=4)

    inputs = [
        "utility theory artificial intelligence",
        "neural networks learn patterns",
        "swarm intelligence distributed systems",
        "reinforcement learning reward systems",
        "emergence complex adaptive systems",
        "distributed cognition shared intelligence"
    ]

    for i in inputs:
        swarm.ingest(i)

        print("\n🌐 SWARM STATE:")
        print(swarm.swarm_state())

        print("🧠 CONSENSUS:", swarm.consensus_strength())
