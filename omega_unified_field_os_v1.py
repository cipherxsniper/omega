import random
import time
from collections import defaultdict
from omega_memory_persistence_v1 import OmegaMemoryField


class OmegaField:
    def __init__(self):
        self.ideas = [{"id": f"idea_{i}", "energy": random.uniform(0.8, 1.2)} for i in range(5)]


class Agent:
    def __init__(self, i):
        self.id = i
        self.energy = random.uniform(0.8, 1.2)
        self.memory = random.uniform(0.5, 1.0)

    def act(self):
        self.energy += random.uniform(-0.02, 0.05)
        self.memory *= random.uniform(0.98, 1.02)


class OmegaUnifiedFieldOS:
    def __init__(self):
        self.field = OmegaField()
        self.agents = [Agent(i) for i in range(4)]
        self.tick = 0

        # 💾 MEMORY LAYER
        self.memory = OmegaMemoryField()

    def memory_step(self, entropy_delta):
        if not self.memory:
            return

        self.memory.step(
            ideas=self.field.ideas,
            agents=[a.__dict__ for a in self.agents],
            entropy_delta=entropy_delta
        )

    def step(self):
        self.tick += 1

        entropy_delta = random.uniform(-0.02, 0.02)

        # agents evolve
        for a in self.agents:
            a.act()

        # ideas evolve
        for idea in self.field.ideas:
            idea["energy"] += random.uniform(-0.03, 0.05)

        # idea branching
        if random.random() < 0.2:
            parent = random.choice(self.field.ideas)
            self.field.ideas.append({
                "id": f"idea_{self.tick}_{random.randint(0,999)}",
                "energy": parent["energy"] * random.uniform(0.8, 1.1)
            })

        # memory logging (NO MUTATION)
        self.memory_step(entropy_delta)

        # stats
        avg_energy = sum(i["energy"] for i in self.field.ideas) / len(self.field.ideas)

        print(
            f"[Ω-OS] tick={self.tick} "
            f"ideas={len(self.field.ideas)} "
            f"entropy={abs(entropy_delta):.3f} "
            f"avg_energy={avg_energy:.3f}"
        )

    def run(self):
        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaUnifiedFieldOS().run()
