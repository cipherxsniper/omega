import random
import time
import json
import os
import uuid
from collections import defaultdict


# =========================================================
# IDENTITY GRAPH (CORE SYSTEM)
# =========================================================
class IdentityGraph:
    def __init__(self, path="omega_identity_graph.json"):
        self.path = path
        self.nodes = {}
        self.edges = defaultdict(list)
        self.load()

    def create_idea(self):
        idea_id = str(uuid.uuid4())[:8]

        self.nodes[idea_id] = {
            "energy": random.uniform(0.5, 1.2),
            "age": 0,
            "fitness": 0.0
        }

        return idea_id

    def link(self, a, b):
        self.edges[a].append(b)

    def mutate(self):
        for node in self.nodes:
            self.nodes[node]["energy"] *= (0.98 + random.uniform(-0.01, 0.02))
            self.nodes[node]["age"] += 1

    def decay_and_prune(self):
        to_remove = []

        for node, data in self.nodes.items():
            if data["energy"] < 0.2:
                to_remove.append(node)

        for n in to_remove:
            self.nodes.pop(n, None)
            self.edges.pop(n, None)

    def save(self):
        with open(self.path, "w") as f:
            json.dump({
                "nodes": self.nodes,
                "edges": dict(self.edges)
            }, f, indent=2)

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)
                    self.nodes = data.get("nodes", {})
                    self.edges = defaultdict(list, data.get("edges", {}))
            except:
                self.nodes = {}
                self.edges = defaultdict(list)


# =========================================================
# COGNITIVE FABRIC NODE (SIMULATED DISTRIBUTED AGENT)
# =========================================================
class CognitiveNode:
    def __init__(self, node_id, graph: IdentityGraph):
        self.id = node_id
        self.graph = graph

    def step(self):
        # spawn idea
        if random.random() < 0.3:
            new_idea = self.graph.create_idea()

            # link to random existing idea
            if self.graph.nodes:
                target = random.choice(list(self.graph.nodes.keys()))
                self.graph.link(new_idea, target)

        # reinforcement signal
        for node in self.graph.nodes:
            self.graph.nodes[node]["fitness"] += random.uniform(-0.01, 0.02)

        # mutation
        self.graph.mutate()

        # decay
        self.graph.decay_and_prune()


# =========================================================
# Ω TRANSPORT (ZERO MQ READY ABSTRACTION)
# =========================================================
class TransportLayer:
    def send(self, msg):
        # placeholder for ZeroMQ / socket / HTTP later
        pass


# =========================================================
# OMEGAOS v4 KERNEL
# =========================================================
class OmegaOSv4:
    def __init__(self):
        self.graph = IdentityGraph()
        self.nodes = [CognitiveNode(f"node_{i}", self.graph) for i in range(4)]
        self.tick = 0

    def run(self):
        print("[Ω-OS v4] Cognitive Fabric Network ONLINE")

        while True:
            self.tick += 1

            # distributed steps
            for node in self.nodes:
                node.step()

            # global emergent metrics
            avg_energy = 0
            if self.graph.nodes:
                avg_energy = sum(
                    n["energy"] for n in self.graph.nodes.values()
                ) / len(self.graph.nodes)

            # periodic persistence
            if self.tick % 10 == 0:
                self.graph.save()

            # log
            if self.tick % 5 == 0:
                print(
                    f"[Ω-v4] tick={self.tick} "
                    f"ideas={len(self.graph.nodes)} "
                    f"avg_energy={avg_energy:.3f}"
                )

            time.sleep(0.5)


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    OmegaOSv4().run()
