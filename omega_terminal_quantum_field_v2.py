import os
import time
import random
import math

SIZE = 40
NODES = 25

colors = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# -----------------------------
# SYSTEM SCAN
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
# PARTICLE (COGNITIVE AGENT)
# -----------------------------
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.jump = 0

    def step(self):
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.5, min(1.5, self.vx))
        self.vy = max(-1.5, min(1.5, self.vy))

        self.x %= SIZE
        self.y %= SIZE

        if random.random() < 0.15:
            self.jump += 1

    def color(self):
        if self.jump == 0:
            return "🟣"
        if self.jump % 7 == 0:
            return "⚪"
        return colors[self.jump % len(colors)]


particles = [Particle(i) for i in range(NODES)]


# -----------------------------
# DISTANCE
# -----------------------------
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)


# -----------------------------
# INFLUENCE FIELD
# -----------------------------
def apply_influence(particles):
    for p in particles:
        fx, fy = 0, 0

        for o in particles:
            if p.id == o.id:
                continue

            d = dist(p, o)
            if d < 0.01:
                continue

            influence = (o.jump + 1) / (d * 0.5)

            if o.jump > p.jump:
                fx += (o.x - p.x) * 0.01 * influence
                fy += (o.y - p.y) * 0.01 * influence
            else:
                fx -= (o.x - p.x) * 0.005 * influence
                fy -= (o.y - p.y) * 0.005 * influence

        p.vx += fx
        p.vy += fy


# -----------------------------
# CLUSTERS
# -----------------------------
def compute_clusters(particles):
    clusters = []
    visited = set()

    for p in particles:
        if p.id in visited:
            continue

        cluster = [p]

        for o in particles:
            if o.id != p.id and dist(p, o) < 5:
                cluster.append(o)
                visited.add(o.id)

        if len(cluster) > 1:
            avg_jump = sum(c.jump for c in cluster) / len(cluster)

            clusters.append({
                "size": len(cluster),
                "avg_jump": avg_jump
            })

    return clusters


# -----------------------------
# RENDER
# -----------------------------
def render():
    total_files, py_files, node_like_files, depth = scan_nodes()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x = int(p.x) % SIZE
        y = int(p.y) % SIZE
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    clusters = compute_clusters(particles)

    print("\n" + "=" * 52)
    print("🧠 OMEGA v2 COGNITIVE INFLUENCE FIELD")
    print("=" * 52)
    print(f"📦 Files        : {total_files}")
    print(f"🐍 Python       : {py_files}")
    print(f"🔗 Nodes        : {node_like_files}")
    print(f"🌐 Depth        : {depth}")
    print("-" * 52)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"🧬 Clusters     : {len(clusters)}")
    print(f"⚡ Total Jumps  : {sum(p.jump for p in particles)}")

    if clusters:
        print("\n📊 Cluster Summary:")
        for i, c in enumerate(clusters[:5]):
            print(f"  Cluster {i}: size={c['size']} avg_jump={c['avg_jump']:.2f}")

    print("=" * 52)


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    for p in particles:
        p.step()

    apply_influence(particles)
    render()
    time.sleep(0.1)
