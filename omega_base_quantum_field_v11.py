# nano_omega_base_quantum_field_v11.py

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
            heatmap[y][x] *= 0.97

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
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y

            dist = math.sqrt(dx*dx + dy*dy) + 0.1
            influence = e["strength"] / dist

            if influence > 0.03:
                self.vx += (dx/dist) * influence * 0.05
                self.vy += (dy/dist) * influence * 0.05

        self.x += self.vx
        self.y += self.vy

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

    # HEAT LAYER
    for y in range(SIZE):
        for x in range(SIZE):
            hc = heat_char(heatmap[y][x])
            if hc:
                grid[y][x] = hc

    # EVENT LAYER
    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    # TRAIL LAYER
    for t in trails:
        grid[t["y"]][t["x"]] = t["color"]

    # PARTICLE LAYER
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

    print("\nKEY:")
    print("🟣🟢🔵⚪ = particle state")
    print("● = quantum return trail")
    print("✦ = signal event")
    print("🟩🟨🟧🟥🔥 = intensity")

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
