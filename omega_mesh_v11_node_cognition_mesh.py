import math
from collections import defaultdict

# -----------------------------
# 🧠 NODE STRUCTURE
# -----------------------------
class Node:
    def __init__(self, name):
        self.name = name
        self.activation = 1.0
        self.connections = defaultdict(float)
        self.last_seen = 0

    def strengthen(self, amount=1.0):
        self.activation += amount

    def decay(self):
        self.activation *= 0.98


# -----------------------------
# 🌐 OMEGA V11 COGNITION MESH
# -----------------------------
class OmegaMeshV11:

    def __init__(self):
        self.nodes = {}
        self.tick = 0

    # -----------------------------
    # 🧩 GET OR CREATE NODE
    # -----------------------------
    def get_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    # -----------------------------
    # 🔗 BUILD CONNECTIONS
    # -----------------------------
    def connect(self, a, b):
        self.nodes[a].connections[b] += 1.0
        self.nodes[b].connections[a] += 1.0

    # -----------------------------
    # 🧠 INGEST QUERY
    # -----------------------------
    def ingest(self, text):
        self.tick += 1

        words = text.lower().split()

        # create nodes
        for w in words:
            self.get_node(w).strengthen()

        # connect sequential concepts
        for i in range(len(words) - 1):
            self.get_node(words[i])
            self.get_node(words[i+1])
            self.connect(words[i], words[i+1])

        # decay old system
        for n in self.nodes.values():
            n.decay()

    # -----------------------------
    # 🔥 COGNITIVE STATE
    # -----------------------------
    def state(self):
        ranked = sorted(
            self.nodes.values(),
            key=lambda n: n.activation,
            reverse=True
        )

        return [
            (n.name, round(n.activation, 3))
            for n in ranked[:10]
        ]

    # -----------------------------
    # 🧠 THINKING ENGINE (GRAPH WALK)
    # -----------------------------
    def think(self, start=None, depth=5):
        if not self.nodes:
            return []

        if not start:
            start = max(self.nodes.values(), key=lambda n: n.activation).name

        path = [start]
        current = self.nodes[start]

        for _ in range(depth):
            if not current.connections:
                break

            next_node = max(
                current.connections.items(),
                key=lambda x: x[1]
            )[0]

            path.append(next_node)
            current = self.nodes[next_node]

        return path


# -----------------------------
# 🚀 RUN DEMO
# -----------------------------
if __name__ == "__main__":
    brain = OmegaMeshV11()

    inputs = [
        "utility theory artificial intelligence",
        "neural networks learn patterns",
        "swarm intelligence distributed systems",
        "reinforcement learning reward systems",
        "emergence complex adaptive systems"
    ]

    for i in inputs:
        brain.ingest(i)
        print("\n🧠 TOP NODES:", brain.state())
        print("🔥 THINK PATH:", brain.think())
