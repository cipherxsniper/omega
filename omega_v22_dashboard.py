import os
import time
import random
import math

# =========================
# NODE (CLUSTER ENTITY)
# =========================

class Node:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(5, 60)
        self.y = random.randint(3, 18)

        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

        self.energy = random.uniform(0.3, 1.0)
        self.pressure = random.uniform(0.2, 0.9)

        self.influence = {}

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.95
        self.vy *= 0.95

        self.pressure += random.uniform(-0.02, 0.02)
        self.pressure = max(0.01, min(1.0, self.pressure))


# =========================
# OMEGA FIELD ENGINE
# =========================

class OmegaField:

    def __init__(self):
        self.nodes = [
            Node("attention"),
            Node("goal"),
            Node("memory"),
            Node("stability")
        ]

        self.events = []

    # -------------------------
    # ENERGY PROPAGATION
    # -------------------------

    def propagate(self):

        for a in self.nodes:
            for b in self.nodes:

                if a == b:
                    continue

                dx = b.x - a.x
                dy = b.y - a.y
                dist = max(0.1, math.sqrt(dx*dx + dy*dy))

                force = (a.pressure * b.pressure) / dist

                a.vx += dx * force * 0.01
                a.vy += dy * force * 0.01

                # causal trace
                self.events.append({
                    "from": a.name,
                    "to": b.name,
                    "weight": round(force, 3)
                })

        self.events = self.events[-15:]  # keep feed clean

    # -------------------------
    # LEADER DETECTION
    # -------------------------

    def leader(self):
        return max(self.nodes, key=lambda n: n.energy * n.pressure)

    # -------------------------
    # RENDER GRID
    # -------------------------

    def render(self):

        os.system("clear")

        print("🧠 OMEGA v22 — COGNITIVE FIELD DASHBOARD\n")

        leader = self.leader()

        grid = [[" " for _ in range(70)] for _ in range(20)]

        # draw nodes
        for n in self.nodes:

            x = int(n.x)
            y = int(n.y)

            if n == leader:
                symbol = "👑"
            else:
                symbol = "●"

            if 0 <= y < 20 and 0 <= x < 70:
                grid[y][x] = symbol

        # print grid
        for row in grid:
            print("".join(row))

        print("\n📊 NODE STATES")

        for n in self.nodes:
            print(f"{n.name:<10} P:{n.pressure:.2f} E:{n.energy:.2f}")

        print("\n🔁 COGNITIVE FLOW")

        for e in self.events[-10:]:
            print(f"{e['from']} → {e['to']} [{e['weight']}]")

        print("\n👑 LEADER:", leader.name)

    # -------------------------
    # UPDATE LOOP
    # -------------------------

    def step(self):

        self.propagate()

        for n in self.nodes:
            n.update()


# =========================
# RUN LOOP
# =========================

if __name__ == "__main__":

    field = OmegaField()

    while True:
        field.step()
        field.render()
        time.sleep(0.2)
