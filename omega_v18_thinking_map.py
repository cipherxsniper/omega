# 🧠 OMEGA v18.5 — CLUSTER PHYSICS + ATTRACTION FIELD ENGINE

import random
import time
import os
import math

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

        self.memory_field = []  # attractor memory trail
        self.is_leader = False

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def record(self):
        self.memory_field.append((self.x, self.y))
        if len(self.memory_field) > 20:
            self.memory_field.pop(0)

    def update_motion(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= FIELD_DECAY
        self.vy *= FIELD_DECAY

        self.pressure += random.uniform(-0.02, 0.02)
        self.pressure = max(0.01, min(1.0, self.pressure))

        self.record()


# -----------------------------
# SYSTEM ENGINE
# -----------------------------

class PhysicsMap:

    def __init__(self):

        self.clusters = [
            Cluster("attention"),
            Cluster("goal"),
            Cluster("memory"),
            Cluster("stability")
        ]

    # -------------------------
    # FORCE CALCULATION
    # -------------------------

    def apply_forces(self):

        for a in self.clusters:
            fx, fy = 0, 0

            for b in self.clusters:

                if a == b:
                    continue

                dx = b.x - a.x
                dy = b.y - a.y
                dist = max(0.1, math.sqrt(dx*dx + dy*dy))

                # attraction (similar pressure = stronger pull)
                attraction = GRAVITY * (a.pressure * b.pressure)

                # repulsion (prevents collapse)
                repulsion = REPULSION / (dist * dist)

                force = attraction - repulsion

                fx += (dx / dist) * force
                fy += (dy / dist) * force

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

                    merged.append(a)
                    merged.append(b)

                    self.clusters.append(new)

        self.clusters = [c for c in self.clusters if c not in merged]

    # -------------------------
    # SPLIT SYSTEM
    # -------------------------

    def handle_splits(self):

        new_clusters = []

        for c in self.clusters:

            instability = abs(c.vx) + abs(c.vy)

            if instability > SPLIT_THRESHOLD and len(self.clusters) < 12:

                child = Cluster(
                    name=c.name + "_split",
                    x=c.x + random.uniform(-1, 1),
                    y=c.y + random.uniform(-1, 1)
                )

                child.energy = c.energy * 0.8
                child.pressure = c.pressure * 0.8

                c.energy *= 0.9
                c.pressure *= 0.9

                new_clusters.append(child)

        self.clusters.extend(new_clusters)

    # -------------------------
    # LEADER SELECTION
    # -------------------------

    def update_leader(self):

        for c in self.clusters:
            c.is_leader = False

        leader = max(self.clusters, key=lambda c: c.energy * c.pressure)
        leader.is_leader = True

    # -------------------------
    # RENDER
    # -------------------------

    def render(self):

        os.system("clear")

        print("🧠 OMEGA v18.5 — PHYSICS FIELD MAP")
        print("=" * 70)

        grid = [[" " for _ in range(75)] for _ in range(25)]

        for c in self.clusters:

            x = int(c.x)
            y = int(c.y)

            symbol = "👑" if c.is_leader else "●"

            if 0 <= y < 25 and 0 <= x < 75:
                grid[y][x] = symbol

            print(f"{symbol} {c.name:<15} P:{c.pressure:.2f} E:{c.energy:.2f}")

        print("\n" + "-" * 70)

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
