# 🧠 OMEGA v20 — ATTRACTOR BRAIN PHYSICS + COGNITIVE FIELDS

import os
import time
import random
import math

# -----------------------------
# COLORS (SEMANTIC PHYSICS)
# -----------------------------

RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
PURPLE = "\033[35m"
YELLOW = "\033[33m"

# -----------------------------
# PARTICLE = INFORMATION FLOW
# -----------------------------

class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.life = 1.0

# -----------------------------
# ATTRACTOR NODE (FIELD NOT OBJECT)
# -----------------------------

class Attractor:

    def __init__(self, name, x, y):

        self.name = name
        self.x = x
        self.y = y

        self.strength = random.uniform(0.4, 0.9)
        self.coherence = random.uniform(0.3, 0.8)
        self.entropy = random.uniform(0.2, 0.6)

        self.resonance = 0.0  # memory persistence field

# -----------------------------
# OMEGA FIELD ENGINE
# -----------------------------

class OmegaField:

    def __init__(self):

        self.nodes = [
            Attractor("goal", 15, 8),
            Attractor("attention", 40, 10),
            Attractor("memory", 55, 16),
            Attractor("stability", 25, 20)
        ]

        self.particles = []

        self.time = 0

    # -------------------------
    # PARTICLE EMISSION (DATA FLOW)
    # -------------------------

    def emit(self):

        for n in self.nodes:

            intensity = n.strength * (1 - n.entropy)

            if random.random() < intensity:

                self.particles.append(
                    Particle(
                        n.x + random.uniform(-1, 1),
                        n.y + random.uniform(-1, 1)
                    )
                )

    # -------------------------
    # ATTRACTOR FORCE FIELD
    # -------------------------

    def field_force(self, p, n):

        dx = n.x - p.x
        dy = n.y - p.y

        dist = max(0.1, math.sqrt(dx*dx + dy*dy))

        # gravitational pull of thought
        pull = (n.strength * n.coherence) / dist

        return dx / dist * pull, dy / dist * pull

    # -------------------------
    # PARTICLE DYNAMICS
    # -------------------------

    def update_particles(self):

        for p in self.particles:

            fx, fy = 0, 0

            for n in self.nodes:

                ax, ay = self.field_force(p, n)

                fx += ax
                fy += ay

                # BASIN FORMATION (resonance capture)
                if abs(ax) + abs(ay) < 0.1:
                    n.resonance += 0.001

            p.vx += fx * 0.05
            p.vy += fy * 0.05

            p.x += p.vx
            p.y += p.vy

            p.life -= 0.02

    # -------------------------
    # ATTRACTOR EVOLUTION
    # -------------------------

    def evolve_nodes(self):

        for n in self.nodes:

            # stable basin deepens
            n.coherence += n.resonance * 0.01

            # entropy decays in stable regions
            n.entropy *= 0.999

            # feedback loop
            if n.resonance > 0.5:
                n.strength += 0.001

            n.strength = max(0.1, min(1.0, n.strength))
            n.coherence = max(0.1, min(1.0, n.coherence))
            n.entropy = max(0.0, min(1.0, n.entropy))

    # -------------------------
    # CLEANUP
    # -------------------------

    def cleanup(self):

        self.particles = [p for p in self.particles if p.life > 0]

    # -------------------------
    # RENDER FIELD
    # -------------------------

    def render(self):

        os.system("clear")

        print("🧠 OMEGA v20 — ATTRACTOR BRAIN PHYSICS")
        print("=" * 70)

        grid = [[" " for _ in range(70)] for _ in range(25)]

        # nodes
        for n in self.nodes:

            x = int(n.x)
            y = int(n.y)

            if n.name == "goal":
                symbol = YELLOW + "G" + RESET
            elif n.name == "stability":
                symbol = GREEN + "S" + RESET
            elif n.name == "attention":
                symbol = CYAN + "A" + RESET
            else:
                symbol = BLUE + "M" + RESET

            if 0 <= x < 70 and 0 <= y < 25:
                grid[y][x] = symbol

        # particles (information flow)
        for p in self.particles:

            x = int(p.x)
            y = int(p.y)

            if 0 <= x < 70 and 0 <= y < 25:
                grid[y][x] = PURPLE + "·" + RESET

        # render
        for row in grid:
            print("".join(row))

        print("\n🟣 particles:", len(self.particles))
        print("🧠 time:", self.time)

    # -------------------------
    # STEP LOOP
    # -------------------------

    def step(self):

        self.emit()
        self.update_particles()
        self.evolve_nodes()
        self.cleanup()

        self.time += 1


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    field = OmegaField()

    while True:
        field.step()
        field.render()
        time.sleep(0.12)
