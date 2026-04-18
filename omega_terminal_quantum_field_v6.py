import os
import time
import random
import math

# =============================
# CONFIG
# =============================
SIZE = 40
NODES = 80

TOP_K = 3
MAX_LINKS = 6

DECAY_WEAK = 0.92
DECAY_STRONG = 0.99

MUTATION_RATE = 0.12

colors = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# =============================
# SYSTEM SCAN
# =============================
def scan_nodes():
    total = 0
    py = 0
    node_like = 0
    depth = 0

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
                    node_like += 1

    return total, py, node_like, depth


# =============================
# NODE = COGNITIVE AGENT
# =============================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.jump = 0

        # 🧠 weighted memory graph
        self.connections = {}

        # 🧬 hierarchical scoring
        self.influence = 0
        self.survival = 1.0
        self.history = 0

    def step(self):
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.5, min(1.5, self.vx))
        self.vy = max(-1.5, min(1.5, self.vy))

        self.x %= SIZE
        self.y %= SIZE

        # mutation event
        if random.random() < MUTATION_RATE:
            self.jump += 1
            self.history += 1

    def color(self):
        if self.influence > 5:
            return "🟣"
        elif self.influence > 2:
            return "🔵"
        elif self.influence > 1:
            return "🟢"
        return "⚪"


# =============================
# DISTANCE
# =============================
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


# =============================
# NODE RANKING (CORE BREAKTHROUGH)
# =============================
def update_ranking(particles):
    for p in particles:
        p.influence = len(p.connections) + p.history * 0.2
        p.survival = 1.0 / (1.0 + math.exp(-p.influence))


# =============================
# ATTENTION SELECTION
# =============================
def update_attention(particles):
    for p in particles:
        scores = []

        for o in particles:
            if p.id == o.id:
                continue

            d = dist(p, o)
            score = (o.influence + 1) / (d + 1)

            scores.append((o, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        selected = scores[:TOP_K]

        total = sum(s for _, s in selected) or 1

        for o, s in selected:
            weight = s / total

            if o.id not in p.connections:
                p.connections[o.id] = 0

            # 🧠 reinforcement memory
            if o.influence > p.influence:
                decay = DECAY_STRONG
            else:
                decay = DECAY_WEAK

            p.connections[o.id] = p.connections[o.id] * decay + weight

        # 🧠 prune weak links
        if len(p.connections) > MAX_LINKS:
            weakest = sorted(p.connections.items(), key=lambda x: x[1])
            for k, _ in weakest[:len(p.connections) - MAX_LINKS]:
                del p.connections[k]


# =============================
# PARTICLE MUTATION CLONING
# =============================
def mutate_particles(particles):
    new_particles = []

    for p in particles:
        if p.influence > 4 and random.random() < 0.05:
            clone = Particle(len(particles) + len(new_particles))
            clone.x = p.x
            clone.y = p.y
            clone.vx = -p.vx
            clone.vy = -p.vy
            clone.history = p.history * 0.5

            new_particles.append(clone)

    particles.extend(new_particles)


# =============================
# RENDER
# =============================
def render(particles):
    total, py, node_like, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x, y = int(p.x), int(p.y)
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    total_links = sum(len(p.connections) for p in particles)
    avg_links = total_links / len(particles)

    top = sorted(particles, key=lambda p: p.influence, reverse=True)[:5]

    print("\n" + "=" * 60)
    print("🧠 OMEGA v6 — HIERARCHICAL MEMORY NETWORK")
    print("=" * 60)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Nodes        : {node_like}")
    print(f"🌐 Depth        : {depth}")
    print("-" * 60)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"🔗 Links        : {total_links}")
    print(f"📊 Avg Links    : {avg_links:.2f}")

    print("\n🧠 Top Hierarchy Nodes:")
    for p in top:
        print(f" Node {p.id} | influence={p.influence:.2f} | links={len(p.connections)}")


# =============================
# INIT
# =============================
particles = [Particle(i) for i in range(NODES)]


# =============================
# MAIN LOOP
# =============================
while True:
    for p in particles:
        p.step()

    update_ranking(particles)
    update_attention(particles)
    mutate_particles(particles)

    render(particles)
    time.sleep(0.1)
