import os
import time
import random
import math
import threading
from collections import deque, defaultdict

# =====================================================
# 🧠 OMEGA v3.1 - EXPANDED COGNITIVE SWARM FIELD
# =====================================================

SIZE = 40
NODES = 80   # 🔥 increased scale

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
# 🧠 BACKGROUND SCANNER (LOW COST)
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
# 🧠 PARTICLE SYSTEM (NOW WITH CONNECTION MEMORY)
# =====================================================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.jump = 0

        # 🧬 memory trail
        self.trail = deque(maxlen=8)

        # 🔗 connection tracking
        self.connections = defaultdict(int)

    def step(self):
        self.trail.append((self.x, self.y))

        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.8, min(1.8, self.vx))
        self.vy = max(-1.8, min(1.8, self.vy))

        if random.random() < 0.10:
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
# 🔗 CONNECTION ENGINE (CORE UPGRADE)
# =====================================================
def update_connections():
    for a in particles:
        for b in particles:
            if a.id == b.id:
                continue

            d = dist(a, b)

            if d < 4:  # interaction radius
                a.connections[b.id] += 1

# =====================================================
# 🧠 INFLUENCE FIELD
# =====================================================
def apply_influence():
    for p in particles:
        fx, fy = 0, 0

        for o in particles:
            if p.id == o.id:
                continue

            d = dist(p, o)
            if d < 0.01:
                continue

            influence = (o.jump + 1) / (d * 0.7)

            if o.jump > p.jump:
                fx += (o.x - p.x) * 0.01 * influence
                fy += (o.y - p.y) * 0.01 * influence
            else:
                fx -= (o.x - p.x) * 0.004 * influence
                fy -= (o.y - p.y) * 0.004 * influence

        p.vx += fx
        p.vy += fy

# =====================================================
# 🧠 CLUSTERS
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
            clusters.append({
                "size": len(group),
                "avg_jump": sum(x.jump for x in group) / len(group)
            })

    return clusters

# =====================================================
# 🎨 RENDER
# =====================================================
def render():
    with lock:
        state = system_state.copy()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x = int(p.x) % SIZE
        y = int(p.y) % SIZE
        grid[y][x] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    clusters = compute_clusters()

    # ============================
    # 🔗 CONNECTION METRICS
    # ============================
    total_connections = sum(sum(p.connections.values()) for p in particles)
    avg_connections = total_connections / NODES

    most_connected = sorted(
        particles,
        key=lambda p: sum(p.connections.values()),
        reverse=True
    )[:3]

    # ============================
    # 🧠 OMEGA INTELLIGENCE PANEL
    # ============================
    print("\n" + "=" * 58)
    print("🧠 OMEGA v3.1 EXPANDED COGNITIVE SWARM FIELD")
    print("=" * 58)

    print(f"📦 Files        : {state['total_files']}")
    print(f"🐍 Python       : {state['py_files']}")
    print(f"🔗 Node Files   : {state['node_like_files']}")
    print(f"🌐 Scan Depth   : {state['depth']}")

    print("-" * 58)
    print(f"🟣 Particles     : {len(particles)}")
    print(f"🧬 Clusters      : {len(clusters)}")
    print(f"⚡ Total Jumps   : {sum(p.jump for p in particles)}")

    print("-" * 58)
    print(f"🔗 Connections   : {total_connections}")
    print(f"📊 Avg Links     : {avg_connections:.2f}")

    print("🔥 Top Connected Nodes:")
    for p in most_connected:
        print(f"   Node {p.id} → {sum(p.connections.values())} links")

    print("=" * 58)

# =====================================================
# 🚀 START SCANNER THREAD
# =====================================================
threading.Thread(target=scan_loop, daemon=True).start()

# =====================================================
# 🔁 MAIN LOOP
# =====================================================
while True:
    for p in particles:
        p.step()

    update_connections()
    apply_influence()
    render()
    time.sleep(0.1)
