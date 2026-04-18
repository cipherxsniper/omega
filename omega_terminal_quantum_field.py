import os
import time
import random

SIZE = 40
NODES = 25

# 🧬 Quantum state colors
# 🟣 origin → 🟢 learning → 🔵 stable → ⚪ coherence/reset
colors = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# -----------------------------
# REAL ECOSYSTEM SCAN
# -----------------------------
def scan_nodes():
    total_files = 0
    py_files = 0
    node_like_files = 0
    depth = 0

    for path in OMEGA_PATHS:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            depth += 1
            for f in files:
                total_files += 1

                if f.endswith(".py"):
                    py_files += 1

                if "node" in f.lower():
                    node_like_files += 1

    return total_files, py_files, node_like_files, depth


# -----------------------------
# PARTICLE SYSTEM (OMEGA AGENT)
# -----------------------------
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.jump = 0
        self.memory = []

    def step(self):
        # movement = cognitive drift
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

        self.x = max(0, min(SIZE - 1, self.x))
        self.y = max(0, min(SIZE - 1, self.y))

        # quantum jump event
        if random.random() < 0.18:
            self.jump += 1
            self.memory.append(self.jump)

    def color(self):
        # 🧠 deterministic evolution (NOT random anymore)
        if self.jump == 0:
            return "🟣"  # origin state

        # white = coherence reset state every 7 jumps
        if self.jump % 7 == 0:
            return "⚪"

        return colors[self.jump % len(colors)]


particles = [Particle(i) for i in range(NODES)]


# -----------------------------
# INTELLIGENCE PANEL
# -----------------------------
def render_panel(total_files, py_files, node_like_files, depth):
    total_jumps = sum(p.jump for p in particles)
    active = len([p for p in particles if p.jump > 0])

    print("\n" + "=" * 52)
    print("🧠 OMEGA LIVE COGNITIVE FIELD v2")
    print("=" * 52)
    print(f"📦 Total Files           : {total_files}")
    print(f"🐍 Python Nodes          : {py_files}")
    print(f"🔗 Node-like Files       : {node_like_files}")
    print(f"🌐 Directory Depth Scan  : {depth}")
    print("-" * 52)
    print(f"🟣 Active Particles      : {len(particles)}")
    print(f"⚡ Total Quantum Jumps   : {total_jumps}")
    print(f"🧬 Active Agents         : {active}")
    print("=" * 52)


# -----------------------------
# FIELD RENDER
# -----------------------------
def render():
    total_files, py_files, node_like_files, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        grid[p.y][p.x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    render_panel(total_files, py_files, node_like_files, depth)


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for p in particles:
        p.step()

    render()
    time.sleep(0.1)
