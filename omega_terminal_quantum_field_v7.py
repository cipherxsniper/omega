import os
import time
import random
import math

# ============================
# CONFIG
# ============================
SIZE = 40
NODES = 90

REGIONS = ["memory", "reasoning", "attention", "explore"]

colors = {
    "memory": "🟣",
    "reasoning": "🔵",
    "attention": "🟢",
    "explore": "⚪"
}

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# ============================
# SCAN SYSTEM
# ============================
def scan_nodes():
    total = py = node = depth = 0

    for path in OMEGA_PATHS:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            depth += 1
            for f in files:
                total += 1
                if f.endswith(".py"):
                    py += 1
                if "node" in f.lower():
                    node += 1

    return total, py, node, depth


# ============================
# NODE
# ============================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.region = random.choice(REGIONS)

        self.influence = 0
        self.connections = {}

    def step(self):
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.2, min(1.2, self.vx))
        self.vy = max(-1.2, min(1.2, self.vy))

    def color(self):
        return colors[self.region]


# ============================
# REGION GRAPH (NEW CORE)
# ============================
def region_similarity(a, b):
    # same region = strong coupling
    return 1.0 if a.region == b.region else 0.3


def update_region_links(particles):
    for p in particles:
        for o in particles:
            if p.id == o.id:
                continue

            sim = region_similarity(p, o)

            if o.id not in p.connections:
                p.connections[o.id] = 0

            # reinforce within region, weaker across regions
            p.connections[o.id] += sim * 0.05

            # decay
            p.connections[o.id] *= 0.98

        # prune weak links
        weak = [k for k,v in p.connections.items() if v < 0.1]
        for k in weak:
            del p.connections[k]


# ============================
# REGION COMMUNICATION LAYER
# ============================
def region_flow(particles):
    region_strength = {r: 0 for r in REGIONS}

    for p in particles:
        region_strength[p.region] += len(p.connections)

    dominant = max(region_strength, key=region_strength.get)

    # bias motion toward dominant region (emergent flow)
    for p in particles:
        if p.region != dominant and random.random() < 0.02:
            p.region = dominant


# ============================
# RENDER
# ============================
def render(particles):
    total, py, node, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x, y = int(p.x), int(p.y)
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    total_links = sum(len(p.connections) for p in particles)
    avg = total_links / len(particles)

    print("\n" + "="*60)
    print("🧠 OMEGA v7 — INTER-REGION COGNITIVE NETWORK")
    print("="*60)
    print(f"📦 Files   : {total}")
    print(f"🐍 Py      : {py}")
    print(f"🔗 Nodes   : {node}")
    print(f"🌐 Depth   : {depth}")
    print("-"*60)
    print(f"🟣 Particles : {len(particles)}")
    print(f"🔗 Links     : {total_links}")
    print(f"📊 Avg Links : {avg:.2f}")

    region_counts = {r:0 for r in REGIONS}
    for p in particles:
        region_counts[p.region] += 1

    print("\n🧠 Region Distribution:")
    for r,v in region_counts.items():
        print(f" {colors[r]} {r}: {v}")


# ============================
# INIT
# ============================
particles = [Particle(i) for i in range(NODES)]


# ============================
# MAIN LOOP
# ============================
while True:
    for p in particles:
        p.step()

    update_region_links(particles)
    region_flow(particles)

    render(particles)
    time.sleep(0.1)
