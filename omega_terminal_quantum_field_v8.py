import os
import time
import random
import math

SIZE = 40
NODES = 90

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

# =========================
# SCAN
# =========================
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


# =========================
# NODE
# =========================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.region = random.choice(REGIONS)

        self.influence = 0

        # weighted graph
        self.links = {}

    def step(self):
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.2, min(1.2, self.vx))
        self.vy = max(-1.2, min(1.2, self.vy))


    def color(self):
        return COLOR[self.region]


# =========================
# DISTANCE
# =========================
def dist(a, b):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)


# =========================
# REGION BIAS CONNECTIONS (FIX)
# =========================
def update_links(particles):
    for p in particles:

        # enforce minimum connectivity
        if len(p.links) < 2:
            candidates = random.sample(particles, 3)
        else:
            candidates = particles

        for o in candidates:
            if p.id == o.id:
                continue

            d = dist(p, o)

            # region interaction logic (CRITICAL FIX)
            region_bias = 1.0

            if p.region == o.region:
                region_bias = 0.6   # discourage redundancy
            else:
                region_bias = 1.4   # encourage cross-region flow

            influence = (1 + o.influence) * region_bias / (d + 1)

            if o.id not in p.links:
                p.links[o.id] = 0

            p.links[o.id] = p.links[o.id] * 0.95 + influence * 0.05

        # prune weak
        weak = [k for k,v in p.links.items() if v < 0.05]
        for k in weak:
            del p.links[k]

        # enforce max links
        if len(p.links) > 6:
            weakest = sorted(p.links.items(), key=lambda x: x[1])
            for k,_ in weakest[:len(p.links)-6]:
                del p.links[k]


# =========================
# INFLUENCE UPDATE
# =========================
def update_influence(particles):
    for p in particles:
        p.influence = len(p.links) * 0.5


# =========================
# EMERGENCE FLOW
# =========================
def region_drift(particles):
    counts = {r:0 for r in REGIONS}

    for p in particles:
        counts[p.region] += len(p.links)

    dominant = max(counts, key=counts.get)

    for p in particles:
        if random.random() < 0.01:
            p.region = dominant


# =========================
# RENDER
# =========================
def render(particles):
    total, py, node, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    total_links = sum(len(p.links) for p in particles)

    print("\n" + "="*60)
    print("🧠 OMEGA v8 — BALANCED INTER-REGION NETWORK")
    print("="*60)
    print(f"📦 Files : {total}")
    print(f"🐍 Py    : {py}")
    print(f"🔗 Nodes : {node}")
    print(f"🌐 Depth : {depth}")
    print("-"*60)
    print(f"🟣 Particles : {len(particles)}")
    print(f"🔗 Links     : {total_links}")
    print("-"*60)

    print("🧠 Region Load:")
    load = {r:0 for r in REGIONS}
    for p in particles:
        load[p.region] += 1

    for k,v in load.items():
        print(f" {COLOR[k]} {k}: {v}")


# =========================
# INIT
# =========================
particles = [Particle(i) for i in range(NODES)]


# =========================
# LOOP
# =========================
while True:
    for p in particles:
        p.step()

    update_links(particles)
    update_influence(particles)
    region_drift(particles)

    render(particles)
    time.sleep(0.1)
