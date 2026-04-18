# 🧠 OMEGA v19.2 — QUANTUM PARTICLE COGNITION MAP

import os
import time
import random
import math

# -----------------------------
# COLORS (SEMANTIC MEANING)
# -----------------------------

RESET = "\033[0m"

GOLD = "\033[33m"      # goal
GREEN = "\033[32m"     # stability
BLUE = "\033[34m"      # memory
CYAN = "\033[36m"      # attention
PURPLE = "\033[35m"    # quantum particles ✨

WHITE = "\033[37m"
RED = "\033[31m"

# -----------------------------
# NODE (COGNITIVE UNIT)
# -----------------------------

class Node:

    def __init__(self, name, x, y):

        self.name = name
        self.x = x
        self.y = y

        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.3, 0.3)

        self.energy = random.uniform(0.3, 0.9)
        self.pressure = random.uniform(0.2, 0.7)

# -----------------------------
# QUANTUM PARTICLE (DATA EVENT)
# -----------------------------

class QuantumParticle:

    def __init__(self, x, y, tx, ty):

        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty

        self.life = 1.0

        self.speed = random.uniform(0.2, 0.6)

    def step(self):

        dx = self.tx - self.x
        dy = self.ty - self.y

        dist = max(0.1, math.sqrt(dx*dx + dy*dy))

        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed

        self.life -= 0.03


# -----------------------------
# BRAIN ENGINE
# -----------------------------

class QuantumBrain:

    def __init__(self):

        self.nodes = [
            Node("goal", 10, 5),
            Node("attention", 30, 10),
            Node("memory", 50, 15),
            Node("stability", 20, 20)
        ]

        self.particles = []
        self.t = 0

    # -------------------------
    # QUANTUM EVENT GENERATION
    # -------------------------

    def emit_particles(self):

        for n in self.nodes:

            if random.random() < n.pressure:

                target = random.choice(self.nodes)

                self.particles.append(
                    QuantumParticle(n.x, n.y, target.x, target.y)
                )

    # -------------------------
    # NODE PHYSICS (MEANINGFUL MOTION)
    # -------------------------

    def update_nodes(self):

        for n in self.nodes:

            # goal pulls system inward
            if n.name == "goal":
                n.vx *= 0.95
                n.vy *= 0.95

            # stability dampens motion
            if n.name == "stability":
                n.vx *= 0.8
                n.vy *= 0.8

            # attention amplifies motion
            if n.name == "attention":
                n.vx += random.uniform(-0.05, 0.05)
                n.vy += random.uniform(-0.05, 0.05)

            n.x += n.vx
            n.y += n.vy

    # -------------------------
    # PARTICLE SYSTEM
    # -------------------------

    def update_particles(self):

        for p in self.particles:
            p.step()

        self.particles = [p for p in self.particles if p.life > 0]

    # -------------------------
    # RENDER
    # -------------------------

    def render(self):

        os.system("clear")

        print("🧠 OMEGA v19.2 — QUANTUM COGNITION FIELD")
        print("=" * 70)

        grid = [[" " for _ in range(70)] for _ in range(25)]

        # nodes
        for n in self.nodes:

            x = int(n.x)
            y = int(n.y)

            if n.name == "goal":
                symbol = GOLD + "G" + RESET
            elif n.name == "stability":
                symbol = GREEN + "S" + RESET
            elif n.name == "attention":
                symbol = CYAN + "A" + RESET
            else:
                symbol = BLUE + "M" + RESET

            if 0 <= x < 70 and 0 <= y < 25:
                grid[y][x] = symbol

        # quantum particles
        for p in self.particles:

            x = int(p.x)
            y = int(p.y)

            if 0 <= x < 70 and 0 <= y < 25:
                grid[y][x] = PURPLE + "·" + RESET

        # render grid
        for row in grid:
            print("".join(row))

        print("\n🟣 quantum particles:", len(self.particles))
        print("🧠 cycle:", self.t)

    # -------------------------
    # UPDATE LOOP
    # -------------------------

    def step(self):

        self.emit_particles()
        self.update_nodes()
        self.update_particles()

        self.t += 1


# -----------------------------
# MAIN LOOP
# -----------------------------

if __name__ == "__main__":

    brain = QuantumBrain()

    while True:
        brain.step()
        brain.render()
        time.sleep(0.12)
