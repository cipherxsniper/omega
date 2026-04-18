# ==================================================
# 🧠 OMEGA v18 — SWARM INTELLIGENCE FIELD
# Particle-to-Particle Communication Upgrade
# ==================================================

import os
import time
import random
import math

SIZE = 40
PARTICLES = 60

# ==================================================
# 🌐 FILE SCAN LAYER
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
# 🌌 GLOBAL FIELD
# ==================================================
FIELD = {
    "pressure": 0.0,
    "entropy": 0.0,
    "coherence": 0.0
}

# ==================================================
# 🌱 MEMORY LAYER
# ==================================================
MEMORY = {
    "messages": 0,
    "syncs": 0
}

# ==================================================
# 🌊 VISUAL BASE COLORS (v11 RESTORED)
# ==================================================
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def particle_color(p):
    return base_colors[(int(p.x + p.y)) % len(base_colors)]


# ==================================================
# 🌌 TRAILS
# ==================================================
trails = []

def add_trail(x, y, symbol):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "symbol": symbol
    })

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# ==================================================
# ⚛️ SWARM PARTICLE SYSTEM (v18 CORE)
# ==================================================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.energy = random.random()

    # ------------------------------------------
    # 🧠 PARTICLE-TO-PARTICLE COMMUNICATION
    # ------------------------------------------
    def communicate(self, others):
        for o in others:
            if o.id == self.id:
                continue

            dx = o.x - self.x
            dy = o.y - self.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1

            # communication radius
            if dist < 6:
                influence = o.energy / dist

                # swarm alignment (real intelligence emergence)
                self.vx += dx * influence * 0.01
                self.vy += dy * influence * 0.01

                # memory sync event
                if influence > 0.2:
                    MEMORY["messages"] += 1
                    add_trail(int(self.x), int(self.y), "✦")

    # ------------------------------------------
    # 🌊 MOTION
    # ------------------------------------------
    def step(self, swarm):
        self.communicate(swarm)

        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.15, 0.15)

        self.x %= SIZE
        self.y %= SIZE

        # quantum trail
        if random.random() < 0.05:
            add_trail(int(self.x), int(self.y), "●")


particles = [Particle(i) for i in range(PARTICLES)]


# ==================================================
# 🌌 FIELD UPDATE
# ==================================================
def update_field():
    FIELD["pressure"] = len(trails) * 0.05
    FIELD["entropy"] *= 0.98
    FIELD["coherence"] = MEMORY["messages"] * 0.001


# ==================================================
# 🧠 SWARM EMERGENCE CHECK
# ==================================================
def swarm_state():
    if FIELD["coherence"] > 0.5:
        return "✦"
    if FIELD["pressure"] > 2:
        return "●"
    return None


# ==================================================
# 🌌 RENDER ENGINE (v11 VISUAL RESTORED)
# ==================================================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # field signal
    sig = swarm_state()
    if sig:
        grid[random.randint(0, SIZE-1)][random.randint(0, SIZE-1)] = sig

    # trails (memory layer)
    for t in trails:
        grid[t["y"]][t["x"]] = t["symbol"]

    # particles
    for p in particles:
        grid[int(p.y)][int(p.x)] = particle_color(p)

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    # ==================================================
    # 🧠 REQUIRED v11 FOOTER (DO NOT REMOVE)
    # ==================================================
    print("\n" + "=" * 50)
    print("🧠 OMEGA v11 — STABILIZED EVENT FIELD")
    print("=" * 50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-" * 50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Jumps        : {MEMORY['messages']}")
    print(f"🌈 Trails       : {len(trails)}")
    print(f"📡 Events       : {MEMORY['messages']}")
    print("=" * 50)


# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:
        for p in particles:
            p.step(particles)

        decay_trails()
        update_field()
        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v18 STOPPED SAFELY")
