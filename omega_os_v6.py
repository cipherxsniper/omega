import random
import time
import json
import os
import uuid
import math
from collections import defaultdict


# =========================================================
# 🧠 SEMANTIC VECTOR UTIL (LIGHTWEIGHT SIMULATION)
# =========================================================
def make_vector():
    return [random.uniform(-1, 1) for _ in range(6)]


def similarity(a, b):
    return 1 / (1 + sum(abs(x - y) for x, y in zip(a, b)))


# =========================================================
# 🧠 SWARM NODE STATE
# =========================================================
class IdeaNode:
    def __init__(self, nid=None):
        self.id = nid or str(uuid.uuid4())[:8]
        self.vector = make_vector()
        self.energy = random.uniform(0.6, 1.2)
        self.fitness = 0.0
        self.age = 0
        self.last_reward = 0.0

    def mutate(self):
        for i in range(len(self.vector)):
            self.vector[i] += random.uniform(-0.05, 0.05)

        self.energy *= (0.99 + random.uniform(-0.01, 0.01))
        self.age += 1


# =========================================================
# 🧠 SWARM GRAPH
# =========================================================
class SwarmGraph:
    def __init__(self, path="omega_v6_swarm.json"):
        self.path = path
        self.nodes = {}
        self.links = defaultdict(list)
        self.load()

    def spawn(self):
        node = IdeaNode()
        self.nodes[node.id] = node
        return node.id

    def link(self, a, b):
        self.links[a].append(b)

    def evolve(self):
        for node in self.nodes.values():
            node.mutate()

    def decay(self):
        remove = []

        for nid, node in self.nodes.items():
            if node.energy < 0.2:
                remove.append(nid)

        for nid in remove:
            self.nodes.pop(nid, None)
            self.links.pop(nid, None)

    def save(self):
        with open(self.path, "w") as f:
            json.dump({
                "nodes": {
                    nid: {
                        "vector": n.vector,
                        "energy": n.energy,
                        "fitness": n.fitness,
                        "age": n.age
                    }
                    for nid, n in self.nodes.items()
                },
                "links": dict(self.links)
            }, f, indent=2)

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)

                for nid, n in data.get("nodes", {}).items():
                    node = IdeaNode(nid)
                    node.vector = n["vector"]
                    node.energy = n["energy"]
                    node.fitness = n["fitness"]
                    node.age = n["age"]
                    self.nodes[nid] = node

                self.links = defaultdict(list, data.get("links", {}))
            except:
                pass


# =========================================================
# 🧠 Ω-LANG v6 (SELF-ADJUSTING RULE ENGINE)
# =========================================================
class OmegaLangV6:
    def __init__(self):
        self.temperature = 1.0  # exploration factor

    def adjust(self, reward_signal):
        # self-modifying behavior
        self.temperature *= (0.99 + reward_signal * 0.02)
        self.temperature = max(0.2, min(2.0, self.temperature))

    def execute(self, graph: SwarmGraph):
        nodes = list(graph.nodes.values())
        if len(nodes) < 2:
            return

        # probabilistic swarm actions
        for node in nodes:
            if random.random() < self.temperature * 0.3:
                graph.spawn()

            if random.random() < self.temperature * 0.2:
                a, b = random.sample(nodes, 2)
                graph.link(a.id, b.id)


# =========================================================
# 🧠 SWARM LEARNING ENGINE
# =========================================================
class SwarmLearning:
    def compute_reward(self, graph: SwarmGraph):
        if not graph.nodes:
            return 0

        energies = [n.energy for n in graph.nodes.values()]
        avg_energy = sum(energies) / len(energies)

        diversity = len(set(tuple(n.vector[:2]) for n in graph.nodes.values()))

        reward = (avg_energy * 0.7) + (diversity * 0.01)
        return reward


# =========================================================
# 🧠 OMEGAOS v6 KERNEL
# =========================================================
class OmegaOSv6:
    def __init__(self):
        self.graph = SwarmGraph()
        self.lang = OmegaLangV6()
        self.learning = SwarmLearning()
        self.tick = 0

    def run(self):
        print("[Ω-OS v6] Swarm Cognitive Network ONLINE")

        while True:
            self.tick += 1

            # evolve system
            self.lang.execute(self.graph)
            self.graph.evolve()
            self.graph.decay()

            # reward signal
            reward = self.learning.compute_reward(self.graph)
            self.lang.adjust(reward)

            # simple fitness propagation
            for node in self.graph.nodes.values():
                node.fitness += reward * 0.01
                node.last_reward = reward

            # persistence
            if self.tick % 10 == 0:
                self.graph.save()

            # logging
            if self.tick % 5 == 0:
                print(
                    f"[Ω-v6] tick={self.tick} "
                    f"nodes={len(self.graph.nodes)} "
                    f"reward={reward:.3f} "
                    f"temp={self.lang.temperature:.3f}"
                )

            time.sleep(0.4)


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    OmegaOSv6().run()
