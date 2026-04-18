import os
import time
import random
import math
from collections import defaultdict

# =============================
# CONFIG
# =============================
SIZE = 50
PARTICLE_COUNT = 120

REGIONS = ["memory", "reasoning", "attention", "explore"]

COLOR = {
    "memory": "🟣",
    "reasoning": "🔵",
    "attention": "🟢",
    "explore": "⚪"
}

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# =============================
# 🧠 CACHED SYSTEM SNAPSHOT (NO MORE os.walk LOOP)
# =============================
def build_snapshot():
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

    return {
        "total_files": total,
        "python_files": py,
        "node_files": node,
        "depth": depth
    }

SNAPSHOT = build_snapshot()

# =============================
# 🧠 PARTICLE (COGNITIVE AGENT)
# =============================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.region = random.choice(REGIONS)

        self.influence = 0
        self.links = {}

        self.energy = random.random()

    def step(self):
        # motion
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        # velocity noise
        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.15, 0.15)

        # clamp
        self.vx = max(-1.2, min(1.2, self.vx))
        self.vy = max(-1.2, min(1.2, self.vy))

        # energy drift
        self.energy += random.uniform(-0.05, 0.05)
        self.energy = max(0, min(1, self.energy))


# =============================
# DISTANCE
# =============================
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


# =============================
# 🧠 ATTENTION-CONSTRAINED LINKING
# =============================
def update_links(particles):
    TOP_K = 4

    for p in particles:
        candidates = random.sample(particles, min(10, len(particles)))

        for o in candidates:
            if p.id == o.id:
                continue

            d = dist(p, o)

            region_bias = 1.3 if p.region != o.region else 0.7

            signal = (o.energy + 0.1) * region_bias / (d + 1)

            p.links[o.id] = p.links.get(o.id, 0) * 0.9 + signal * 0.1

        # prune weak
        p.links = {k: v for k, v in p.links.items() if v > 0.05}

        # enforce TOP-K attention (CRITICAL FIX)
        if len(p.links) > TOP_K:
            strongest = dict(sorted(p.links.items(), key=lambda x: x[1], reverse=True)[:TOP_K])
            p.links = strongest


# =============================
# INFLUENCE UPDATE
# =============================
def update_influence(particles):
    for p in particles:
        p.influence = sum(p.links.values())


# =============================
# REGION EVOLUTION
# =============================
def evolve_regions(particles):
    load = defaultdict(int)

    for p in particles:
        load[p.region] += p.influence

    dominant = max(load, key=load.get)

    for p in particles:
        if random.random() < 0.01:
            p.region = dominant


# =============================
# RENDER ENGINE
# =============================
def render(particles):
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        grid[int(p.y)][int(p.x)] = COLOR[p.region]

    os.system("clear")

    for row in grid:
        print("".join(row))

    total_links = sum(len(p.links) for p in particles)

    print("\n" + "=" * 60)
    print("🧠 OMEGA v9 — NON-BLOCKING COGNITIVE ENGINE")
    print("=" * 60)

    print(f"📦 Files        : {SNAPSHOT['total_files']}")
    print(f"🐍 Python       : {SNAPSHOT['python_files']}")
    print(f"🔗 Node Files   : {SNAPSHOT['node_files']}")
    print(f"🌐 Depth        : {SNAPSHOT['depth']}")
    print("-" * 60)

    print(f"🟣 Particles    : {len(particles)}")
    print(f"🔗 Links        : {total_links}")
    print("-" * 60)

    region_count = defaultdict(int)
    for p in particles:
        region_count[p.region] += 1

    print("🧠 Region Distribution:")
    for r in REGIONS:
        print(f" {COLOR[r]} {r}: {region_count[r]}")


# =============================
# INIT
# =============================
particles = [Particle(i) for i in range(PARTICLE_COUNT)]


# =============================
# MAIN LOOP (NO BLOCKING IO)
# =============================
while True:
    for p in particles:
        p.step()

    update_links(particles)
    update_influence(particles)
    evolve_regions(particles)

    render(particles)
    time.sleep(0.08)
