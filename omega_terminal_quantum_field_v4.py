import os
import time
import random
import math
import threading
from collections import defaultdict, deque

# =====================================================
# 🧠 OMEGA v4 - ATTENTION-BASED COGNITIVE NETWORK
# =====================================================

SIZE = 40
NODES = 80

colors = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# =====================================================
# 🌐 SYSTEM STATE CACHE
# =====================================================
system_state = {
    "total_files": 0,
    "py_files": 0,
    "node_like_files": 0,
    "depth": 0
}

lock = threading.Lock()

# =====================================================
# 🧠 BACKGROUND SCANNER (SAFE + LIGHTWEIGHT)
# =====================================================
def scan_loop():
    global system_state

    while True:
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

        with lock:
            system_state = {
                "total_files": total_files,
                "py_files": py_files,
                "node_like_files": node_like_files,
                "depth": depth
            }

        time.sleep(5)

# =====================================================
# 🧠 PARTICLE (COGNITIVE NODE)
# =====================================================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.jump = 0

        # 🧬 MEMORY TRAIL
        self.trail = deque(maxlen=8)

        # 🔗 WEIGHTED CONNECTIONS (KEY UPGRADE)
        self.connections = defaultdict(float)

        # 🧠 STABLE IDENTITY SEED
        self.identity = random.random()

    def step(self):
        self.trail.append((self.x, self.y))

        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.15, 0.15)

        self.vx = max(-1.6, min(1.6, self.vx))
        self.vy = max(-1.6, min(1.6, self.vy))

        if random.random() < 0.1:
            self.jump += 1

    def color(self):
        if self.jump == 0:
            return "🟣"
        if self.jump % 7 == 0:
            return "⚪"
        return colors[self.jump % len(colors)]

# =====================================================
# 🧠 INIT PARTICLES
# =====================================================
particles = [Particle(i) for i in range(NODES)]

# =====================================================
# 📏 DISTANCE
# =====================================================
def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# =====================================================
# ⚡ CONNECTION UPDATE (WEIGHTED LEARNING)
# =====================================================
def update_connections():
    for a in particles:
        for b in particles:
            if a.id == b.id:
                continue

            d = dist(a, b)

            if d < 4:
                # reinforcement learning
                a.connections[b.id] += 1 / (d + 0.1)

# =====================================================
# 🧠 DECAY SYSTEM (FORGETTING)
# =====================================================
def decay_connections():
    for p in particles:
        for k in list(p.connections.keys()):
            p.connections[k] *= 0.97

            if p.connections[k] < 0.1:
                del p.connections[k]

# =====================================================
# 🧠 TOP-K ATTENTION FILTER
# =====================================================
def get_attention(p, k=5):
    sorted_links = sorted(
        p.connections.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_links[:k]

# =====================================================
# 🧠 INFLUENCE FIELD (ATTENTION DRIVEN)
# =====================================================
def apply_influence():
    for p in particles:
        fx, fy = 0, 0

        attention = get_attention(p, 5)
        attention_ids = {x[0] for x in attention}

        for o in particles:
            if p.id == o.id:
                continue

            d = dist(p, o)
            if d < 0.01:
                continue

            # ONLY strong connections influence motion
            weight = p.connections.get(o.id, 0)

            influence = (o.jump + 1 + weight) / (d + 0.5)

            if o.id in attention_ids:
                fx += (o.x - p.x) * 0.02 * influence
                fy += (o.y - p.y) * 0.02 * influence
            else:
                fx -= (o.x - p.x) * 0.005 * influence
                fy -= (o.y - p.y) * 0.005 * influence

        p.vx += fx
        p.vy += fy

# =====================================================
# 🧠 CLUSTER PERSISTENCE (IDENTITY BASED)
# =====================================================
def compute_clusters():
    clusters = []
    visited = set()

    for p in particles:
        if p.id in visited:
            continue

        group = [p]

        for o in particles:
            if o.id != p.id and dist(p, o) < 5:
                group.append(o)
                visited.add(o.id)

        if len(group) > 1:
            stable_hash = sum(x.identity for x in group) / len(group)

            clusters.append({
                "size": len(group),
                "identity": stable_hash,
                "avg_jump": sum(x.jump for x in group) / len(group)
            })

    return clusters

# =====================================================
# 🎨 RENDER SYSTEM
# =====================================================
def render():
    with lock:
        state = system_state.copy()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x = int(p.x)
        y = int(p.y)
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    clusters = compute_clusters()

    total_connections = sum(len(p.connections) for p in particles)

    print("\n" + "=" * 60)
    print("🧠 OMEGA v4 - ATTENTION-BASED COGNITIVE NETWORK")
    print("=" * 60)

    print(f"📦 Files        : {state['total_files']}")
    print(f"🐍 Python       : {state['py_files']}")
    print(f"🔗 Node Files   : {state['node_like_files']}")
    print(f"🌐 Depth        : {state['depth']}")

    print("-" * 60)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"🧬 Clusters     : {len(clusters)}")
    print(f"⚡ Jumps        : {sum(p.jump for p in particles)}")
    print(f"🔗 Connections  : {total_connections}")

    print("-" * 60)
    print("🧠 Top Attention Nodes:")

    top = sorted(particles, key=lambda p: len(p.connections), reverse=True)[:3]
    for t in top:
        print(f"  Node {t.id} → {len(t.connections)} strong links")

    print("=" * 60)

# =====================================================
# 🚀 START SCANNER
# =====================================================
threading.Thread(target=scan_loop, daemon=True).start()

# =====================================================
# 🔁 MAIN LOOP
# =====================================================
while True:
    for p in particles:
        p.step()

    update_connections()
    decay_connections()
    apply_influence()
    render()

    time.sleep(0.1)
