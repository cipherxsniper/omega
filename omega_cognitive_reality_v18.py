import time
import random
import math
import uuid


# =========================
# 🧩 IDEA OBJECT
# =========================
class Idea:

    def __init__(self, x, y):

        self.id = str(uuid.uuid4())[:8]

        self.x = x
        self.y = y

        self.strength = random.uniform(0.3, 1.0)
        self.stability = random.uniform(0.3, 1.0)

    def reinforce(self, value):
        self.strength += value
        self.strength = min(self.strength, 5.0)


# =========================
# 🧠 PHYSICS BRAIN
# =========================
class Brain:

    def __init__(self, brain_id):

        self.id = brain_id

        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)

        self.vx = 0
        self.vy = 0

        self.mass = random.uniform(0.5, 2.0)
        self.reward = 0.0

    def move(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.9
        self.vy *= 0.9

    def apply_force(self, fx, fy):

        self.vx += fx / self.mass
        self.vy += fy / self.mass


# =========================
# 🌌 REALITY FIELD
# =========================
class CognitiveReality:

    def __init__(self, n=6):

        self.brains = [Brain(f"brain_{i}") for i in range(n)]
        self.ideas = []

        self.tick = 0

    # -------------------------
    # DISTANCE
    # -------------------------
    def dist(self, a, b):

        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2) + 0.01

    # -------------------------
    # IDEA CREATION
    # -------------------------
    def spawn_idea(self):

        if random.random() < 0.3:

            b = random.choice(self.brains)

            idea = Idea(b.x, b.y)
            self.ideas.append(idea)

    # -------------------------
    # IDEA REINFORCEMENT
    # -------------------------
    def reinforce_ideas(self):

        for idea in self.ideas:

            for b in self.brains:

                d = self.dist(idea, b)

                if d < 0.5:
                    idea.reinforce(0.05)

    # -------------------------
    # MEMORY ANCHORS
    # -------------------------
    def apply_memory_field(self):

        for idea in self.ideas:

            if idea.strength > 2.0:

                for b in self.brains:

                    d = self.dist(idea, b)

                    if d < 1.0:
                        # pull brain toward stable idea
                        fx = (idea.x - b.x) * 0.01
                        fy = (idea.y - b.y) * 0.01
                        b.apply_force(fx, fy)

    # -------------------------
    # CLUSTERS → BELIEFS
    # -------------------------
    def belief_systems(self):

        clusters = []

        for idea in self.ideas:

            group = []

            for other in self.ideas:

                if self.dist(idea, other) < 0.5:
                    group.append(other)

            if len(group) > 2:

                coherence = sum(i.strength for i in group) / len(group)

                clusters.append({
                    "size": len(group),
                    "coherence": round(coherence, 2)
                })

        return clusters

    # -------------------------
    # STEP
    # -------------------------
    def step(self):

        self.tick += 1

        self.spawn_idea()
        self.reinforce_ideas()
        self.apply_memory_field()

        for b in self.br
