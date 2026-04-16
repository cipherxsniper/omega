import time
import random


# =========================
# 🧬 IDENTITY NODE
# =========================
class IdentityNode:

    def __init__(self, node_id, parents=None):

        self.id = node_id
        self.parents = parents or []

        self.strength = random.uniform(0.3, 1.0)
        self.age = 0
        self.mutations = 0

    def mutate(self):

        self.strength += random.uniform(-0.05, 0.05)
        self.strength = max(0.0, min(1.0, self.strength))

        self.mutations += 1


# =========================
# 🧠 IDENTITY GRAPH ENGINE
# =========================
class IdentityGraph:

    def __init__(self):

        self.nodes = {}

    # -------------------------
    # CREATE OR UPDATE NODE
    # -------------------------
    def create(self, node_id, parents=None):

        if node_id not in self.nodes:
            self.nodes[node_id] = IdentityNode(node_id, parents)

        return self.nodes[node_id]

    # -------------------------
    # FUSION RULE
    # -------------------------
    def fuse(self, id_a, id_b):

        if id_a not in self.nodes or id_b not in self.nodes:
            return None

        a = self.nodes[id_a]
        b = self.nodes[id_b]

        # similarity check (simple heuristic)
        similarity = 1 - abs(a.strength - b.strength)

        if similarity > 0.7:

            new_id = f"fusion_{id_a}_{id_b}_{int(time.time())}"

            child = IdentityNode(
                new_id,
                parents=[id_a, id_b]
            )

            child.strength = (a.strength + b.strength) / 2

            self.nodes[new_id] = child

            print(f"[Ω-GRAPH] fused {id_a} + {id_b} → {new_id}")

            return new_id

        return None

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def evolve(self):

        for node in list(self.nodes.values()):

            node.age += 1

            node.mutate()

            # decay weak nodes
            if node.strength < 0.2:
                print(f"[Ω-GRAPH] pruning {node.id}")
                del self.nodes[node.id]

    # -------------------------
    # DEBUG PRINT
    # -------------------------
    def status(self):

        return {
            "nodes": len(self.nodes),
            "strongest": max(self.nodes.values(), key=lambda n: n.strength).id
            if self.nodes else None
        }


# =========================
# 🚀 DEMO LOOP
# =========================
if __name__ == "__main__":

    graph = IdentityGraph()

    # seed ideas
    for i in range(5):
        graph.create(f"idea_{i}")

    tick = 0

    while True:

        tick += 1

        graph.evolve()

        # random fusion attempts
        keys = list(graph.nodes.keys())

        if len(keys) > 1:
            a, b = random.sample(keys, 2)
            graph.fuse(a, b)

        print("[Ω-GRAPH]", graph.status())

        time.sleep(0.5)
