# ==================================================
# 🧠 OMEGA v20 — SWARM MEMORY MESH
# Particle-to-Particle Intelligence Propagation
# ==================================================

import random
import math
import os
import time

SIZE = 40
PARTICLES = 60

# ==================================================
# 🌐 FILE SYSTEM FEED (REAL DATA ANCHOR)
# ==================================================
def scan_files():
    total = py = node = 0

    paths = [
        os.path.expanduser("~/Omega"),
        os.path.expanduser("~/Omega/omega-bot")
    ]

    for path in paths:
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path):
            for f in files:
                total += 1
                if f.endswith(".py"):
                    py += 1
                if "node" in f.lower():
                    node += 1

    return total, py, node


# ==================================================
# 🧠 SWARM MEMORY MODEL
# ==================================================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        # 🧠 MEMORY CORE (THIS IS THE BREAKTHROUGH)
        self.memory = random.random()
        self.influence = random.random()

        self.has_jumped = False

    # ------------------------------------------
    # 🌊 SWARM COMMUNICATION (CORE FEATURE)
    # ------------------------------------------
    def communicate(self, others):
        for o in others:
            if o.id == self.id:
                continue

            dist = abs(self.x - o.x) + abs(self.y - o.y)

            if dist < 4:
                # memory diffusion (bidirectional)
                transfer = (self.memory - o.memory) * 0.05

                self.memory -= transfer
                o.memory += transfer

                # influence ripple
                self.influence += o.influence * 0.01

    # ------------------------------------------
    # ⚛️ MOTION SYSTEM
    # ------------------------------------------
    def step(self):
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        self.x += self.vx
        self.y += self.vy

        self.x %= SIZE
        self.y %= SIZE

        # quantum drift
        if random.random() < 0.04:
            self.memory *= 1.05


particles = [Particle(i) for i in range(PARTICLES)]


# ==================================================
# 🌈 VISUAL SYSTEM (v11 CONTRACT RESTORED)
# ==================================================
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def color(p):
    return base_colors[int(p.memory * 10 + p.id) % len(base_colors)]


# ==================================================
# 🌊 RENDER ENGINE
# ==================================================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # PARTICLE COMMUNICATION STEP FIRST
    for p in particles:
        p.communicate(particles)

    # MOTION STEP
    for p in particles:
        p.step()

        x = int(p.x)
        y = int(p.y)
        grid[y][x] = color(p)

    # DISPLAY
    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    # ==================================================
    # 🧠 REQUIRED v11 FOOTER (LOCKED CONTRACT)
    # ==================================================
    print("\n" + "=" * 50)
    print("🧠 OMEGA v11 — STABILIZED EVENT FIELD")
    print("=" * 50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("--------------------------------------------------")
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Swarm Memory Active")
    print(f"🌐 Communication Mesh: ON")
    print("=" * 50)


# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:
        render()
        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v20 STOPPED SAFELY")
