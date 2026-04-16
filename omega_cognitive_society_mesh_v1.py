import random
import time
from collections import defaultdict


# -------------------------
# IDEA OBJECT
# -------------------------
class Idea:
    def __init__(self, i):
        self.id = f"idea_{i}"
        self.energy = random.uniform(0.8, 1.2)
        self.age = 0

    def mutate(self):
        self.energy += random.uniform(-0.05, 0.05)
        self.age += 1


# -------------------------
# NODE (AGENT BRAIN)
# -------------------------
class Node:
    def __init__(self, i):
        self.id = f"node_{i}"
        self.ideas = [Idea(f"{i}_{j}") for j in range(4)]
        self.weight = random.uniform(0.8, 1.2)

    def local_think(self):
        for idea in self.ideas:
            idea.mutate()

        # spawn new ideas
        if random.random() < 0.3:
            self.ideas.append(Idea(f"{self.id}_{random.randint(0,999)}"))


# -------------------------
# MESH SYSTEM
# -------------------------
class OmegaMesh:
    def __init__(self):
        self.nodes = [Node(i) for i in range(5)]
        self.global_memory = defaultdict(float)
        self.tick = 0

    # -------------------------
    # CROSS NODE IDEA MIGRATION
    # -------------------------
    def migrate_ideas(self):
        for node in self.nodes:
            if len(node.ideas) == 0:
                continue

            idea = random.choice(node.ideas)
            target = random.choice(self.nodes)

            if target != node:
                target.ideas.append(idea)

    # -------------------------
    # VOTING MEMORY SYSTEM
    # -------------------------
    def update_memory(self):
        self.global_memory.clear()

        for node in self.nodes:
            for idea in node.ideas:
                self.global_memory[idea.id] += idea.energy * node.weight

        # normalize memory field
        total = sum(self.global_memory.values()) + 1e-9
        for k in self.global_memory:
            self.global_memory[k] /= total

    # -------------------------
    # SELECTION PRESSURE
    # -------------------------
    def collapse_system(self):
        for node in self.nodes:
            node.ideas = [
                idea for idea in node.ideas
                if self.global_memory.get(idea.id, 0) > 0.02
            ]

    # -------------------------
    # IDENTITY FIELD (EMERGENT)
    # -------------------------
    def identity_signature(self):
        top = sorted(
            self.global_memory.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return [i[0] for i in top]

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        for node in self.nodes:
            node.local_think()

        self.migrate_ideas()
        self.update_memory()
        self.collapse_system()

        identity = self.identity_signature()

        print(
            f"[Ω-MESH] tick={self.tick} "
            f"nodes={len(self.nodes)} "
            f"ideas={sum(len(n.ideas) for n in self.nodes)} "
            f"identity={identity}"
        )

    def run(self):
        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaMesh().run()
