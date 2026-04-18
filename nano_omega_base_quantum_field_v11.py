import os
import time
import random
import sys
import math

SIZE = 40
PARTICLES = 60

# =========================
# FILE SCAN CACHE
# =========================
_SCAN_CACHE = {"time": 0, "data": (0, 0, 0)}
CACHE_TTL = 3.0

def scan_files():
    global _SCAN_CACHE
    now = time.time()

    if now - _SCAN_CACHE["time"] < CACHE_TTL:
        return _SCAN_CACHE["data"]

    total = py = node = 0

    paths = [
        os.path.expanduser("~/Omega"),
        os.path.expanduser("~/Omega/omega-bot")
    ]

    for path in paths:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            for f in files:
                total += 1
                if f.endswith(".py"):
                    py += 1
                if "node" in f.lower():
                    node += 1

    _SCAN_CACHE["time"] = now
    _SCAN_CACHE["data"] = (total, py, node)
    return total, py, node


# =========================
# VISUAL SYSTEMS
# =========================
def rainbow_dot():
    colors = [31,32,33,34,35,36,91,92,93,94,95,96]
    return f"\033[{random.choice(colors)}m●\033[0m"


heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def update_heat(x, y):
    heatmap[y][x] += 1

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] = heatmap[y][x] * 0.93 + random.random() * 0.02


def heat_char(v):
    if v > 50: return "🔥"
    if v > 30: return "🟥"
    if v > 15: return "🟧"
    if v > 8:  return "🟨"
    if v > 3:  return "🟩"
    return None


# =========================
# TRAILS
# =========================
trails = []

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# =========================
# EVENT BUS
# =========================
events = []

def emit_event(x, y, strength):
    events.append({
        "x": x,
        "y": y,
        "strength": strength,
        "life": 8
    })

def decay_events():
    for e in events:
        e["life"] -= 1
        e["strength"] *= 0.88
    events[:] = [e for e in events if e["life"] > 0]


# =========================
# PARTICLE SYSTEM
# =========================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.jump = 0

    def step(self):
        # center field pressure
        cx, cy = SIZE / 2, SIZE / 2
        self.vx += (cx - self.x) * 0.0005
        self.vy += (cy - self.y) * 0.0005

        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y

            dist = math.sqrt(dx*dx + dy*dy) + 0.1
            influence = e["strength"] / dist

            if influence > 0.015:
                self.vx += (dx/dist) * influence * 0.12
                self.vy += (dy/dist) * influence * 0.12

        self.x += self.vx
        self.y += self.vy

        # energy damping
        self.vx *= 0.995
        self.vy *= 0.995

        self.vx += random.uniform(-0.15, 0.15)
        self.vy += random.uniform(-0.15, 0.15)

        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 1.5:
            self.vx *= 0.7
            self.vy *= 0.7

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        if random.random() < 0.07:
            self.jump += 1

            trails.append({
                "x": int(self.x),
                "y": int(self.y),
                "life": random.randint(4, 7),
                "color": rainbow_dot()
            })

            emit_event(
                int(self.x),
                int(self.y),
                random.uniform(0.8, 2.0)
            )

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[self.jump % len(base)]


particles = [Particle(i) for i in range(PARTICLES)]


# =========================
# RENDER SYSTEM
# =========================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(SIZE):
        for x in range(SIZE):
            hc = heat_char(heatmap[y][x])
            if hc:
                grid[y][x] = hc

    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    for t in trails:
        if random.random() > 0.3:
            grid[t["y"]][t["x"]] = t["color"]

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    print("\n" + "="*50)
    print("🧠 OMEGA v11 — STABILIZED EVENT FIELD")
    print("="*50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-"*50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Total Jumps  : {sum(p.jump for p in particles)}")
    print(f"🌈 Trails       : {len(trails)}")
    print(f"📡 Events       : {len(events)}")
    print("="*50)

    sys.stdout.flush()


# =========================
# MAIN LOOP
# =========================
try:
    while True:
        for p in particles:
            p.step()

        decay_trails()
        decay_events()
        decay_heat()

        render()
        time.sleep(0.15)

except KeyboardInterrupt:
    print("\n🧠 Omega stopped safely.")

# =========================
# 🧠 v12 COGNITIVE LAYER
# =========================

bonds = set()
clusters = []


# =========================
# 🧠 v12 COGNITIVE LAYER
# =========================

bonds = set()
clusters = []


# --- v12 MEMORY EXTENSION ---
self.memory = [0.0, 0.0, 0.0]
self.experience = 0


# --- v12 MEMORY UPDATE ---
self.memory[0] = self.memory[0] * 0.95 + self.vx * 0.05
self.memory[1] = self.memory[1] * 0.95 + self.vy * 0.05
self.memory[2] = self.memory[2] * 0.95 + (len(events) * 0.01)
self.experience += 1


# --- v12 BOND FORMATION RULES ---
for other in particles:
    if other.id == self.id:
        continue

    dx = self.x - other.x
    dy = self.y - other.y
    dist = (dx*dx + dy*dy) ** 0.5

    similarity = abs(self.memory[0] - other.memory[0]) + abs(self.memory[1] - other.memory[1])

    if dist < 3 and similarity < 0.3:
        bonds.add(tuple(sorted((self.id, other.id))))


# =========================
# 🧠 CLUSTER ENGINE v12
# =========================

def build_clusters():
    visited = set()
    clusters.clear()

    for p in particles:
        if p.id in visited:
            continue

        cluster = []
        stack = [p]

        while stack:
            cur = stack.pop()
            if cur.id in visited:
                continue

            visited.add(cur.id)
            cluster.append(cur)

            for a, b in bonds:
                if a == cur.id:
                    stack.append(particles[b])
                elif b == cur.id:
                    stack.append(particles[a])

        clusters.append(cluster)


# --- v12 INTERACTION-BASED DECAY ---
# Replace old life/time decay logic with:
decay_factor = 1.0 / (1 + getattr(p, "experience", 1) * 0.01)


# =========================
# ⚡ CLUSTER ENERGY MODEL
# =========================

def compute_cluster_energy(cluster):
    return sum(p.vx*p.vx + p.vy*p.vy for p in cluster)

def stabilize_clusters():
    for c in clusters:
        energy = compute_cluster_energy(c)

        if energy > 5:
            for p in c:
                p.vx *= 0.99
                p.vy *= 0.99


# =========================
# 🧠 v12 LOOP INTEGRATION PATCH
# =========================

# ADD THIS INSIDE YOUR MAIN WHILE LOOP
# right AFTER: for p in particles: p.step()

build_clusters()
stabilize_clusters()


# =========================
# 🧠 v13 INTENT SYSTEM
# =========================

cluster_intent = {}  # cluster_id → [dx, dy]
cluster_reward = {}  # cluster_id → scalar score


# Example global attractor (you can change dynamically)
GLOBAL_GOAL = (20, 20)

def compute_goal_vector(cx, cy):
    gx, gy = GLOBAL_GOAL
    dx = gx - cx
    dy = gy - cy
    mag = (dx*dx + dy*dy) ** 0.5 + 0.0001
    return dx/mag, dy/mag


    # =========================
    # v13 INTENT ASSIGNMENT
    # =========================

    cx = sum(p.x for p in cluster) / len(cluster)
    cy = sum(p.y for p in cluster) / len(cluster)

    cluster_id = len(clusters)

    cluster_intent[cluster_id] = compute_goal_vector(cx, cy)
    cluster_reward[cluster_id] = 0


# =========================
# v13 INTENT INJECTION
# =========================

for cid, cluster in enumerate(clusters):
    if self in cluster:
        intent = cluster_intent.get(cid, (0, 0))

        # apply weak directional pressure
        self.vx += intent[0] * 0.02
        self.vy += intent[1] * 0.02


# =========================
# v13 REWARD SYSTEM
# =========================

def update_cluster_rewards():
    for cid, cluster in enumerate(clusters):
        cx = sum(p.x for p in cluster) / len(cluster)
        cy = sum(p.y for p in cluster) / len(cluster)

        gx, gy = GLOBAL_GOAL
        dist = ((gx-cx)**2 + (gy-cy)**2) ** 0.5

        cluster_reward[cid] += max(0, 10 - dist)

