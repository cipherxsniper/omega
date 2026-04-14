import random
import time
from collections import defaultdict
from omega_memory_persistence_v1 import OmegaMemoryField


# -------------------------
# IDEA OBJECT
# -------------------------
class Idea:
    def __init__(self, i, energy):
        self.id = f"idea_{i}"
        self.energy = energy
        self.age = 0
        self.history_weight = random.uniform(0.5, 1.0)

    def fitness(self):
        # identity persistence emerges from history + energy
        return (self.energy * 0.6) + (self.history_weight * 0.4)


# -------------------------
# AGENT OBJECT
# -------------------------
class Agent:
    def __init__(self, i):
        self.id = i
        self.energy = random.uniform(0.8, 1.2)
        self.memory_bias = random.uniform(0.5, 1.0)

    def act(self):
        self.energy += random.uniform(-0.02, 0.05)
        self.memory_bias *= random.uniform(0.99, 1.01)


# -------------------------
# OMEGA FIELD
# -------------------------
class OmegaField:
    def __init__(self):
        self.ideas = [Idea(i, random.uniform(0.8, 1.2)) for i in range(6)]


# -------------------------
# OMEGA FEEDBACK SYSTEM
# -------------------------
class OmegaFeedbackOS:
    def __init__(self):
        self.field = OmegaField()
        self.agents = [Agent(i) for i in range(4)]
        self.tick = 0

        # memory layer (observational only)
        self.memory = OmegaMemoryField()

    # -------------------------
    # CORE EVOLUTION LOGIC
    # -------------------------
    def evolve_ideas(self):

        avg_fitness = sum(i.fitness() for i in self.field.ideas) / len(self.field.ideas)

        new_ideas = []

        for idea in self.field.ideas:
            idea.age += 1

            # MEMORY INFLUENCE (KEY FEATURE)
            memory_pressure = idea.history_weight * 0.02

            # entropy force
            entropy = random.uniform(-0.03, 0.03)

            # survival dynamics
            idea.energy += entropy + memory_pressure

            # decay of forgotten ideas
            idea.energy -= (idea.age * 0.001)

            # idea collapse
            if idea.energy < 0.3:
                continue

            # idea branching
            if random.random() < 0.15 + (idea.history_weight * 0.1):
                child = Idea(
                    i=f"{idea.id}_{self.tick}",
                    energy=idea.energy * random.uniform(0.8, 1.1)
                )
                child.history_weight = idea.history_weight * random.uniform(0.95, 1.05)
                new_ideas.append(child)

            new_ideas.append(idea)

        self.field.ideas = new_ideas

    # -------------------------
    # AGENT EVOLUTION
    # -------------------------
    def evolve_agents(self):
        for a in self.agents:
            a.act()

    # -------------------------
    # MEMORY (OBSERVATIONAL ONLY)
    # -------------------------
    def memory_step(self):
        self.memory.step(
            ideas=[i.__dict__ for i in self.field.ideas],
            agents=[a.__dict__ for a in self.agents],
            entropy_delta=random.uniform(-0.02, 0.02)
        )

    # -------------------------
    # MAIN LOOP
    # -------------------------
    def step(self):
        self.tick += 1

        self.evolve_agents()
        self.evolve_ideas()
        self.memory_step()

        avg_energy = sum(i.energy for i in self.field.ideas) / len(self.field.ideas)

        dominant = max(self.field.ideas, key=lambda x: x.fitness()).id

        print(
            f"[Ω-FEEDBACK] tick={self.tick} "
            f"ideas={len(self.field.ideas)} "
            f"avg_energy={avg_energy:.3f} "
            f"dominant={dominant}"
        )

    def run(self):
        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaFeedbackOS().run()
