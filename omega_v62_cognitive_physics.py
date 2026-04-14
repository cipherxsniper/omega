import random
import math
from collections import defaultdict


# =========================
# 🌌 IDEA SPACE (PHYSICS FIELD)
# =========================
class IdeaField:
    def __init__(self):
        self.mass = defaultdict(lambda: 1.0)        # idea strength
        self.velocity = defaultdict(float)          # momentum of change

    def reinforce(self, idea, amount):
        self.mass[idea] += amount
        self.velocity[idea] += amount * 0.1

    def decay(self):
        for k in list(self.mass.keys()):
            self.mass[k] *= 0.995
            self.velocity[k] *= 0.90

            if self.mass[k] < 0.05:
                del self.mass[k]
                del self.velocity[k]


# =========================
# 🌪️ ENTROPY FIELD
# =========================
class EntropyField:
    def __init__(self):
        self.value = 1.0

    def update(self, diversity):
        # more diversity = more entropy
        target = min(2.0, max(0.3, diversity))

        self.value += (target - self.value) * 0.05


# =========================
# 🧲 COGNITIVE GRAVITY
# =========================
class GravityField:
    def force(self, idea_mass, entropy):
        # gravity increases with mass, decreases with entropy
        return idea_mass / (1.0 + entropy)


# =========================
# 🧠 AGENT
# =========================
class PhysicsAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.energy = random.uniform(0.8, 1.2)
        self.focus = random.choice(["attention", "memory", "goal", "stability"])

    def perceive(self, idea_field, gravity_field, entropy):
        forces = {}

        for idea, mass in idea_field.mass.items():
            force = gravity_field.force(mass, entropy)

            # attention bias
            if idea == self.focus:
                force *= 1.2

            forces[idea] = force

        return forces

    def act(self, forces):
        if not forces:
            return None

        chosen = max(forces, key=forces.get)

        # energy cost of cognition
        self.energy -= 0.02

        # energy gain from alignment
        self.energy += forces[chosen] * 0.01

        return chosen


# =========================
# 🌌 PHYSICS SYSTEM
# =========================
class CognitivePhysicsSystem:
    def __init__(self):
        self.agents = [PhysicsAgent(i) for i in range(6)]

        self.ideas = IdeaField()
        self.entropy = EntropyField()
        self.gravity = GravityField()

        self.tick = 0

        # seed ideas
        for i in ["attention", "memory", "goal", "stability"]:
            self.ideas.mass[i] = random.uniform(0.5, 1.5)

    def step(self):
        self.tick += 1

        chosen_ideas = defaultdict(int)

        # diversity metric
        diversity = len(self.ideas.mass) / 10.0
        self.entropy.update(diversity)

        # agent interactions
        for agent in self.agents:
            forces = agent.perceive(
                self.ideas,
                self.gravity,
                self.entropy.value
            )

            idea = agent.act(forces)

            if idea:
                chosen_ideas[idea] += 1
                self.ideas.reinforce(idea, 0.05)

        # physics evolution
        self.ideas.decay()

        avg_energy = sum(a.energy for a in self.agents) / len(self.agents)

        print(
            f"[V62] tick={self.tick} "
            f"ideas={len(self.ideas.mass)} "
            f"entropy={self.entropy.value:.3f} "
            f"avg_energy={avg_energy:.3f} "
            f"dominant={max(chosen_ideas, key=chosen_ideas.get) if chosen_ideas else None}"
        )


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    system = CognitivePhysicsSystem()

    while True:
        system.step()
