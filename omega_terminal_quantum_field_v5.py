import os
import time
import random
import math

# =============================
# CONFIG (SPARSE INTELLIGENCE CORE)
# =============================
SIZE = 40
NODES = 80

TOP_K = 3
MAX_LINKS = 6
DECAY = 0.97

colors = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# =============================
# SYSTEM SCAN (REAL DATA)
# =============================
def scan_nodes():
    total_files = 0
    py_files = 0
    node_like = 0
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
                    node_like += 1

    return total_files, py_files, node_like, depth


# =============================
# PARTICLE = COGNITIVE NODE
# =============================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.jump = 0

        # 🧠 sparse memory graph
        self.connections = {}

    def step(self):
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.5, min(1.5, self.vx))
        self.vy = max(-1.5, min(1.5, self.vy))

        self.x %= SIZE
        self.y %= SIZE

        if random.random() < 0.12:
            self.jump += 1

    def color(self):
        return colors[self.jump % len(colors)]


# =============================
# DISTANCE
# =============================
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


# =============================
# SOFTMAX NORMALIZATION
# =============================
def softmax(weights):
    if not weights:
        return []

    m = max(weights)
    exps = [math.exp(w - m) for w in weights]
    s = sum(exps)
    return [e / s for e in exps]


# =============================
# COMPETITIVE ATTENTION UPDATE
# =============================
def update_attention(particles):
    for p in particles:
        scores = []

        for o in particles:
            if p.id == o.id:
                continue

            d = dist(p, o)
            if d < 0.1:
                continue

            # interaction score = similarity + activity bias
            score = (o.jump + 1) / (d + 1)
            scores.append((o, score))

        # sort competitors
        scores.sort(key=lambda x: x[1], reverse=True)

        # 🧠 TOP-K ATTENTION SELECTION (COMPETITION)
        selected = scores[:TOP_K]

        weights = [s for _, s in selected]
        norm = softmax(weights)

        # update connections
        for (o, _), w in zip(selected, norm):
            p.connections[o.id] = p.connections.get(o.id, 0) * DECAY + w

        # 🧠 PRUNE WEAK LINKS
        if len(p.connections) > MAX_LINKS:
            weakest = sorted(p.connections.items(), key=lambda x: x[1])
            for k, _ in weakest[:len(p.connections) - MAX_LINKS]:
                del p.connections[k]


# =============================
# PARTICLE FIELD
# =============================
particles = [Particle(i) for i in range(NODES)]


# =============================
# RENDER FIELD
# =============================
def render():
    total_files, py_files, node_like, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x, y = int(p.x), int(p.y)
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    # =============================
    # INTELLIGENCE PANEL
    # =============================
    total_links = sum(len(p.connections) for p in particles)

    avg_links = total_links / len(particles)

    top_hubs = sorted(
        particles,
        key=lambda p: len(p.connections),
        reverse=True
    )[:5]

    print("\n" + "=" * 60)
    print("🧠 OMEGA v5 COMPETITIVE COGNITIVE NETWORK")
    print("=" * 60)
    print(f"📦 Files        : {total_files}")
    print(f"🐍 Python       : {py_files}")
    print(f"🔗 Node Files   : {node_like}")
    print(f"🌐 Depth        : {depth}")
    print("-" * 60)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"🔗 Total Links  : {total_links}")
    print(f"📊 Avg Links    : {avg_links:.2f}")
    print(f"⚡ Active Hubs  : {len(top_hubs)}")

    print("\n🧠 Top Cognitive Hubs:")
    for h in top_hubs:
        print(f"  Node {h.id} → {len(h.connections)} links")


# =============================
# MAIN LOOP
# =============================
while True:
    for p in particles:
        p.step()

    update_attention(particles)
    render()

    time.sleep(0.1)
