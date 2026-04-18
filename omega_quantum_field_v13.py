import os
import time
import random
import sys
import math

SIZE = 40
PARTICLES = 60

# =========================
# FILE SCAN CACHE (UNCHANGED v11)
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
# TRAILS (UNCHANGED)
# =========================
trails = []

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# =========================
# EVENTS
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
# 🧠 v13 SWARM MEMORY FIELD (NEW)
# =========================
swarm_memory = {
    "avg_vx": 0,
    "avg_vy": 0,
    "pressure": 0
}


# =========================
# 🧬 v13 ENTROPY ENGINE
# =========================
def field_entropy(x, y, vx, vy, heat):
    return (
        (math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1 +
        (vx * vy) * 0.01 +
        heat * 0.0001
    )


# =========================
# PARTICLE SYSTEM (v13 UPGRADED ONLY HERE)
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

        heat = heatmap[int(self.y)][int(self.x)]
        q = field_entropy(self.x, self.y, self.vx, self.vy, heat)

        # EVENT FORCE
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y
            d = math.sqrt(dx*dx + dy*dy) + 0.1

            influence = e["strength"] / d
            self.vx += (dx/d) * influence * 0.05
            self.vy += (dy/d) * influence * 0.05

        # VECTOR MEMORY
        self.memory.append((self.vx, self.vy))
        if len(self.memory) > 5:
            self.memory.pop(0)

        mem_vx = sum(m[0] for m in self.memory) / len(self.memory)
        mem_vy = sum(m[1] for m in self.memory) / len(self.memory)

        # SWARM COORDINATION
        for p in particles:
            if p is not self:
                dx = p.x - self.x
                dy = p.y - self.y
                d = math.sqrt(dx*dx + dy*dy) + 0.1

                if d < 6:
                    self.vx += dx / d * 0.01
                    self.vy += dy / d * 0.01

        # SWARM MEMORY INJECTION
        self.vx += swarm_memory["avg_vx"] * 0.02
        self.vy += swarm_memory["avg_vy"] * 0.02

        # QUANTUM DRIFT (STATE BASED)
        self.vx += q * 0.2 + mem_vx * 0.05
        self.vy += q * 0.2 + mem_vy * 0.05

        # POSITION UPDATE
        self.x += self.vx
        self.y += self.vy

        # RANDOM MICRO NOISE
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        # ENTROPY CONTROL
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 1.6:
            self.vx *= 0.8
            self.vy *= 0.8

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        # SWARM MEMORY UPDATE
        swarm_memory["avg_vx"] = (swarm_memory["avg_vx"] + self.vx) * 0.5
        swarm_memory["avg_vy"] = (swarm_memory["avg_vy"] + self.vy) * 0.5

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[self.jump % len(base)]


particles = [Particle(i) for i in range(PARTICLES)]


# =========================
# RENDER (UNCHANGED CONTRACT)
# =========================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # HEAT
    for y in range(SIZE):
        for x in range(SIZE):
            hc = heat_char(heatmap[y][x])
            if hc:
                grid[y][x] = hc

    # EVENTS
    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    # TRAILS
    for t in trails:
        grid[t["y"]][t["x"]] = t["color"]

    # PARTICLES
    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    print("\n" + "="*50)
    print("🧠 OMEGA v13 — ASIF FIELD")
    print("="*50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-"*50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Jumps        : {sum(p.jump for p in particles)}")
    print(f"🌈 Trails       : {len(trails)}")
    print(f"📡 Events       : {len(events)}")
    print("="*50)


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
