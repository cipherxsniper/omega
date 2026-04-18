# 🧠 OMEGA v19 — PHYSICS + SEMANTIC OBSERVABILITY ENGINE

import random
import time
import os
import math

# -----------------------------
# COLORS (ANSI)
# -----------------------------

RESET = "\033[0m"
GOLD = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RED = "\033[31m"
BLUE = "\033[34m"

# -----------------------------
# PHYSICS CONSTANTS
# -----------------------------

GRAVITY = 0.8
REPULSION = 1.2
MERGE_DISTANCE = 3
SPLIT_THRESHOLD = 0.85
FIELD_DECAY = 0.97


# -----------------------------
# CLUSTER OBJECT
# -----------------------------

class Cluster:

    def __init__(self, name, x=None, y=None):

        self.name = name
        self.x = x if x is not None else random.randint(10, 60)
        self.y = y if y is not None else random.randint(5, 20)

        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

        self.energy = random.uniform(0.3, 0.9)
        self.pressure = random.uniform(0.2, 0.6)

        self.memory_field = []
        self.is_leader = False

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def update_motion(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= FIELD_DECAY
        self.vy *= FIELD_DECAY

        self.pressure += random.uniform(-0.02, 0.02)
        self.pressure = max(0.01, min(1.0, self.pressure))


# -----------------------------
# PHYSICS + COGNITION ENGINE
# -----------------------------

class PhysicsMap:

    def __init__(self):

        self.clusters = [
            Cluster("attention"),
            Cluster("goal"),
            Cluster("memory"),
            Cluster("stability")
        ]

        self.connections = []   # (A -> B influence)
        self.history = []

    # -------------------------
    # FORCE SYSTEM
    # -------------------------

    def apply_forces(self):

        self.connections.clear()

        for a in self.clusters:
            fx, fy = 0, 0

            for b in self.clusters:

                if a == b:
                    continue

                dx = b.x - a.x
                dy = b.y - a.y
                dist = max(0.1, math.sqrt(dx*dx + dy*dy))

                attraction = GRAVITY * (a.pressure * b.pressure)
                repulsion = REPULSION / (dist * dist)

                force = attraction - repulsion

                fx += (dx / dist) * force
                fy += (dy / dist) * force

                # store influence connection
                self.connections.append((a.name, b.name, round(force, 3)))

            a.vx += fx * 0.05
            a.vy += fy * 0.05

    # -------------------------
    # MERGE SYSTEM
    # -------------------------

    def handle_merges(self):

        merged = []

        for i in range(len(self.clusters)):
            for j in range(i + 1, len(self.clusters)):

                a = self.clusters[i]
                b = self.clusters[j]

                if a in merged or b in merged:
                    continue

                if a.distance(b) < MERGE_DISTANCE:

                    new = Cluster(
                        name=f"{a.name}_{b.name}",
                        x=(a.x + b.x) / 2,
                        y=(a.y + b.y) / 2
                    )

                    new.energy = (a.energy + b.energy) / 2
                    new.pressure = (a.pressure + b.pressure) / 2

                    merged.extend([a, b])
                    self.clusters.append(new)

        self.clusters = [c for c in self.clusters if c not in merged]

    # -------------------------
    # SPLIT SYSTEM
    # -------------------------

    def handle_splits(self):

        new_nodes = []

        for c in self.clusters:

            instability = abs(c.vx) + abs(c.vy)

            if instability > SPLIT_THRESHOLD and len(self.clusters) < 14:

                child = Cluster(
                    name=c.name + "_split",
                    x=c.x + random.uniform(-1, 1),
                    y=c.y + random.uniform(-1, 1)
                )

                child.energy = c.energy * 0.85
                child.pressure = c.pressure * 0.85

                new_nodes.append(child)

        self.clusters.extend(new_nodes)

    # -------------------------
    # LEADER SYSTEM
    # -------------------------

    def update_leader(self):

        for c in self.clusters:
            c.is_leader = False

        leader = max(self.clusters, key=lambda c: c.energy * c.pressure)
        leader.is_leader = True

    # -------------------------
    # SENTENCE GENERATOR (NEW)
    # -------------------------

    def generate_sentence(self):

        leader = max(self.clusters, key=lambda c: c.energy * c.pressure)

        avg_pressure = sum(c.pressure for c in self.clusters) / len(self.clusters)

        if leader.name.startswith("goal"):
            role = "system is converging toward objective formation"
        elif avg_pressure > 0.6:
            role = "system is in high-energy exploratory state"
        else:
            role = "system is stabilizing internal structure"

        return f"🧠 {leader.name} is dominant; {role}."

    # -------------------------
    # RENDER
    # -------------------------

    def render(self):

        os.system("clear")

        print("🧠 OMEGA v19 — SEMANTIC PHYSICS BRAIN")
        print("=" * 80)

        # SYSTEM STATS BAR
        avg_p = sum(c.pressure for c in self.clusters) / len(self.clusters)
        avg_e = sum(c.energy for c in self.clusters) / len(self.clusters)

        print(f"📊 NODES:{len(self.clusters)}  PRESSURE:{avg_p:.2f}  ENERGY:{avg_e:.2f}")
        print("-" * 80)

        grid = [[" " for _ in range(80)] for _ in range(25)]

        # render clusters
        for c in self.clusters:

            x = int(c.x)
            y = int(c.y)

            if c.name == "goal":
                symbol = GOLD + "●" + RESET
            elif c.name == "stability":
                symbol = GREEN + "●" + RESET
            elif c.is_leader:
                symbol = RED + "👑" + RESET
            else:
                symbol = CYAN + "●" + RESET

            if 0 <= y < 25 and 0 <= x < 80:
                grid[y][x] = symbol

            print(f"{symbol} {c.name:<15} P:{c.pressure:.2f} E:{c.energy:.2f}")

        print("\n" + "-" * 80)

        # sentence output
        print(self.generate_sentence())

        print("\n" + "-" * 80)

        # connection summary
        print("🔗 ACTIVE CONNECTIONS (sample):")
        for c in self.connections[:8]:
            print(f"{c[0]} → {c[1]} [{c[2]}]")

        print("-" * 80)

        # grid
        for row in grid:
            print("".join(row))

    # -------------------------
    # UPDATE LOOP
    # -------------------------

    def step(self):

        self.apply_forces()

        for c in self.clusters:
            c.update_motion()

        self.handle_merges()
        self.handle_splits()
        self.update_leader()


# -----------------------------
# MAIN LOOP
# -----------------------------

if __name__ == "__main__":

    sim = PhysicsMap()

    while True:
        sim.step()
        sim.render()
        time.sleep(0.2)
