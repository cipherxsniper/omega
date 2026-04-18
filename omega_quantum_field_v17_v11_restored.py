# ==================================================
# 🧠 OMEGA v11 — STABILIZED EVENT FIELD (VISUAL CORE)
# 🧠 OMEGA v17 — SWARM MEMORY MESH (FUSED)
# ==================================================

import random
import math
import uuid
import os

SIZE = 40
PARTICLES = 60

# ==================================================
# 🧠 MEMORY + SWARM SYSTEM
# ==================================================
particles = []
memory_mesh = {}

# ==================================================
# 🌈 v11 BASE COLORS (DO NOT REMOVE)
# ==================================================
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def particle_color(p):
    return base_colors[(int(p["x"]) + int(p["y"])) % len(base_colors)]

# ==================================================
# 🟥 HEATMAP (v11 SQUARE FIELD RESTORE)
# ==================================================
heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def heat_char(v):
    if v > 30: return "🟥"
    if v > 20: return "🟧"
    if v > 10: return "🟨"
    if v > 5:  return "🟩"
    return None

def update_heat(x, y):
    heatmap[y][x] += 2

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= 0.95

# ==================================================
# 🌊 TRAILS (v11 QUANTUM RETURN VISUALS)
# ==================================================
trails = []

def add_trail(x, y, returning=False):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "returning": returning,
        "color": "✦" if random.random() < 0.5 else "●"
    })

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

# ==================================================
# 🧠 PARTICLE MODEL
# ==================================================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.uniform(0, SIZE-1)
        self.y = random.uniform(0, SIZE-1)
        self.vx = random.uniform(-0.6, 0.6)
        self.vy = random.uniform(-0.6, 0.6)

        self.jump = 0
        self.memory = random.random()
        self.returning = False

    def communicate(self, other):
        dist = abs(self.x - other.x) + abs(self.y - other.y)

        if dist < 5:
            shared = (self.memory + other.memory) / 2
            self.memory = shared
            other.memory = shared

    def step(self):
        self.x += self.vx
        self.y += self.vy

        # bounce + return marker
        if self.x <= 0 or self.x >= SIZE-1:
            self.vx *= -1
            self.returning = True

        if self.y <= 0 or self.y >= SIZE-1:
            self.vy *= -1
            self.returning = True

        # quantum jump
        if random.random() < 0.08:
            self.jump += 1
            add_trail(int(self.x), int(self.y), self.returning)
            self.memory *= 1.02

        update_heat(int(self.x), int(self.y))

# ==================================================
# 🧠 INIT PARTICLES
# ==================================================
particles = [Particle(i) for i in range(PARTICLES)]

# ==================================================
# 🌐 FILE SCAN (REAL DATA ANCHOR)
# ==================================================
def scan_files():
    total = py = node = 0

    for path in ["~/Omega"]:
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            for f in files:
                total += 1
                if f.endswith(".py"):
                    py += 1
                if "node" in f:
                    node += 1

    return total, py, node

# ==================================================
# 🔗 SWARM MESH
# ==================================================
def swarm():
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            particles[i].communicate(particles[j])

# ==================================================
# 🌌 RENDER ENGINE (v11 RESTORED PRIORITY ORDER)
# ==================================================
def render():

    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # 1. HEATMAP FIRST (SQUARE FIELD)
    for y in range(SIZE):
        for x in range(SIZE):
            c = heat_char(heatmap[y][x])
            if c:
                grid[y][x] = c

    # 2. TRAILS (QUANTUM MEMORY)
    for t in trails:
        x = int(t["x"])
        y = int(t["y"])
        grid[y][x] = t["color"]

    # 3. PARTICLES (BASE IDENTITY)
    for p in particles:
        x = int(p.x)
        y = int(p.y)

        if p.returning:
            grid[y][x] = "✦"
        else:
            grid[y][x] = particle_color({"x": p.x, "y": p.y})

    # OUTPUT FIELD
    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    # ==================================================
    # 🧠 REQUIRED v11 FOOTER (LOCKED CONTRACT)
    # ==================================================
    print("\n" + "="*50)
    print("🧠 OMEGA v11 — STABILIZED EVENT FIELD")
    print("="*50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-"*50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Jumps        : {sum(p.jump for p in particles)}")
    print(f"🌈 Trails      : {len(trails)}")
    print(f"📡 Events      : ACTIVE")
    print("="*50)

# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:

        for p in particles:
            p.step()

        swarm()
        decay_trails()
        decay_heat()
        render()

except KeyboardInterrupt:
    print("\n🧠 OMEGA STOPPED SAFELY")
