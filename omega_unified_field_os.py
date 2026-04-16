import random
import math
import time
import threading

# =========================
# Ω GLOBAL FIELD
# =========================

class OmegaField:
    def __init__(self):
        self.ideas = []
        self.agents = []
        self.entropy = 0.35
        self.tick = 0
        self.lock = threading.Lock()

    def register_agent(self, agent):
        self.agents.append(agent)

    def seed(self, n=5):
        for i in range(n):
            self.ideas.append(Idea(
                id=f"idea_{i}",
                energy=random.uniform(0.5, 1.5),
                complexity=random.uniform(0.2, 1.0)
            ))

# =========================
# IDEA OBJECT (physics unit)
# =========================

class Idea:
    def __init__(self, id, energy, complexity):
        self.id = id
        self.energy = energy
        self.complexity = complexity
        self.age = 0

    def __repr__(self):
        return f"{self.id}(E={self.energy:.2f}, C={self.complexity:.2f})"


# =========================
# AGENT (cognitive unit)
# =========================

class Agent:
    def __init__(self, id):
        self.id = id
        self.energy = random.uniform(0.8, 1.2)
        self.influence = random.uniform(0.5, 1.0)

    def perceive(self, field: OmegaField):
        if not field.ideas:
            return None
        return random.choice(field.ideas)

    def act(self, field: OmegaField):
        idea = self.perceive(field)
        if not idea:
            return

        # influence idea energy
        delta = self.influence * 0.02
        idea.energy += delta

        # agent gains feedback
        self.energy += delta * 0.5

        # cost of cognition
        self.energy -= 0.01


# =========================
# FIELD PHYSICS ENGINE
# =========================

class PhysicsEngine:
    def step(self, field: OmegaField):

        # -------------------------
        # ENTROPY DYNAMICS
        # -------------------------
        field.entropy += (random.random() - 0.5) * 0.03
        field.entropy = max(0.05, min(field.entropy, 1.0))

        # -------------------------
        # IDEA EVOLUTION
        # -------------------------
        new_ideas = []

        for idea in field.ideas:
            idea.age += 1

            # GRAVITY: ideas attract each other
            attraction = sum(
                other.energy * 0.001
                for other in field.ideas
                if other != idea
            )
            idea.energy += attraction

            # ENTROPY FLUCTUATION
            idea.energy += (random.random() - 0.5) * field.entropy * 0.05

            # BRANCHING
            if random.random() < field.entropy * 0.15:
                new_ideas.append(Idea(
                    id=f"{idea.id}_child_{idea.age}",
                    energy=idea.energy * 0.5,
                    complexity=min(1.0, idea.complexity + 0.1)
                ))

            # COLLAPSE / SPLIT
            if idea.energy > 2.5:
                idea.energy *= 0.5
                new_ideas.append(Idea(
                    id=f"{idea.id}_split_{idea.age}",
                    energy=idea.energy,
                    complexity=idea.complexity
                ))

        field.ideas.extend(new_ideas)

        # prune weak ideas
        field.ideas = [i for i in field.ideas if i.energy > 0.1]


# =========================
# UNIFIED SYSTEM CORE
# =========================

class OmegaUnifiedOS:
    def __init__(self):
        self.field = OmegaField()
        self.physics = PhysicsEngine()

        self.field.seed(6)

        for i in range(4):
            self.field.register_agent(Agent(f"agent_{i}"))

    def step(self):
        self.field.tick += 1

        # agents act
        for agent in self.field.agents:
            agent.act(self.field)

        # physics evolves universe
        self.physics.step(self.field)

        avg_energy = sum(i.energy for i in self.field.ideas) / max(1, len(self.field.ideas))

        dominant = max(self.field.ideas, key=lambda x: x.energy).id if self.field.ideas else "none"

        print(
            f"[Ω-OS] tick={self.field.tick} "
            f"ideas={len(self.field.ideas)} "
            f"entropy={self.field.entropy:.3f} "
            f"avg_energy={avg_energy:.3f} "
            f"dominant={dominant}"
        )

    def run(self):
        while True:
            with self.field.lock:
                self.step()
            time.sleep(0.5)


if __name__ == "__main__":
    OmegaUnifiedOS().run()
