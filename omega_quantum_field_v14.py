import os
import time
import random
import sys
import math

SIZE = 40
PARTICLES = 60

# =========================
# FILE SCAN CACHE (v11 preserved)
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
# HEAT SYSTEM (UNCHANGED)
# =========================
heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def update_heat(x, y):
    heatmap[y][x] += 1

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= 0.97

def heat_char(v):
    if v > 50: return "🔥"
    if v > 30: return "🟥"
    if v > 15: return "🟧"
    if v > 8:  return "🟨"
    if v > 3:  return "🟩"
    return None


# =========================
# TRAILS + EVENTS (UNCHANGED)
# =========================
trails = []
events = []

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

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
# 🧠 v14 HIERARCHY SYSTEM (NEW CORE)
# =========================
leaders = []

def compute_score(p):
    hx = int(p.x) % SIZE
    hy = int(p.y) % SIZE
    heat = heatmap[hy][hx]

    return (
        abs(p.vx) +
        abs(p.vy) +
        heat * 0.01
    )

def update_hierarchy():
    global leaders

    scored = [(compute_score(p), p) for p in particles]
    scored.sort(key=lambda x: x[0], reverse=True)

    leaders = [p for _, p in scored[:5]]


# =========================
# PARTICLE SYSTEM (v14 ONLY ADDITION IS HIERARCHY)
# =========================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.jump = 0
        self.memory = []

    def step(self):

        # EVENT FIELD
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y
            d = math.sqrt(dx*dx + dy*dy) + 0.1

            influence = e["strength"] / d
            self.vx += (dx/d) * influence * 0.05
            self.vy += (dy/d) * influence * 0.05

        # MEMORY
        self.memory.append((self.vx, self.vy))
        if len(self.memory) > 5:
            self.memory.pop(0)

        mem_vx = sum(m[0] for m in self.memory) / len(self.memory)
        mem_vy = sum(m[1] for m in self.memory) / len(self.memory)

        # SWARM COHESION
        for p in particles:
            if p is not self:
                dx = p.x - self.x
                dy = p.y - self.y
                d = math.sqrt(dx*dx + dy*dy) + 0.1

                if d < 6:
                    self.vx += dx / d * 0.01
                    self.vy += dy / d * 0.01

        # 🧠 HIERARCHY FORCE (v14 ADDITION)
        for l in leaders:
            dx = l.x - self.x
            dy = l.y - self.y
            d = math.sqrt(dx*dx + dy*dy) + 0.1

            if self not in leaders:
                self.vx += dx / d * 0.02
                self.vy += dy / d * 0.02

        # QUANTUM DRIFT
        q = random.random() * 0.2
        self.vx += q + mem_vx * 0.05
        self.vy += q + mem_vy * 0.05

        # POSITION
        self.x += self.vx
        self.y += self.vy

        # NOISE
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        # STABILITY
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 1.6:
            self.vx *= 0.8
            self.vy *= 0.8

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[self.jump % len(base)]


particles = [Particle(i) for i in range(PARTICLES)]


# =========================
# RENDER (UNCHANGED CONTRACT)
# =========================
def render():
    total = py = node = 0
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
        grid[t["y"]][t["x"]] = t["color"]

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    print("\n" + "="*50)
    print("🧠 OMEGA v14 — SWARM HIERARCHY LAYER")
    print("="*50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-"*50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"👑 Leaders      : {len(leaders)}")
    print(f"🌈 Trails       : {len(trails)}")
    print(f"📡 Events       : {len(events)}")
    print("="*50)


# =========================
# MAIN LOOP
# =========================
try:
    while True:
        update_hierarchy()

        for p in particles:
            p.step()

        decay_trails()
        decay_events()
        decay_heat()

        render()
        time.sleep(0.15)

except KeyboardInterrupt:
    print("\n🧠 Omega stopped safely.")
