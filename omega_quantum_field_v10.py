import os
import time
import random
import math
import sys

# =========================
# CONFIG
# =========================
SIZE = 40
PARTICLES = 60

# =========================
# FILE SCAN CACHE (NON-BLOCKING)
# =========================
_SCAN_CACHE = {"time": 0, "data": (0, 0, 0)}
CACHE_TTL = 3.0

def scan_files():
    global _SCAN_CACHE
    now = time.time()

    if now - _SCAN_CACHE["time"] < CACHE_TTL:
        return _SCAN_CACHE["data"]

    total = 0
    py = 0
    node = 0

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
# RAINBOW DOT (RETURN SIGNAL)
# =========================
def rainbow_dot():
    colors = [31,32,33,34,35,36,91,92,93,94,95,96]
    return f"\033[{random.choice(colors)}m●\033[0m"


# =========================
# TRAILS (EVENT MEMORY)
# =========================
trails = []


# =========================
# PARTICLE
# =========================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1,1)
        self.vy = random.uniform(-1,1)

        self.jump = 0

    def step(self):
        # movement
        self.x += self.vx
        self.y += self.vy

        # noise
        self.vx += random.uniform(-0.2,0.2)
        self.vy += random.uniform(-0.2,0.2)

        # clamp
        self.vx = max(-1.2, min(1.2, self.vx))
        self.vy = max(-1.2, min(1.2, self.vy))

        # wrap
        self.x %= SIZE
        self.y %= SIZE

        # quantum jump
        if random.random() < 0.08:
            self.jump += 1

            # create return trail
            trails.append({
                "x": int(self.x),
                "y": int(self.y),
                "life": random.randint(3,6),
                "color": rainbow_dot()
            })

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[self.jump % len(base)]


particles = [Particle(i) for i in range(PARTICLES)]


# =========================
# RENDER
# =========================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # draw trails FIRST (event layer)
    for t in trails:
        if 0 <= t["x"] < SIZE and 0 <= t["y"] < SIZE:
            grid[t["y"]][t["x"]] = t["color"]

    # draw particles (state layer)
    for p in particles:
        x = int(p.x)
        y = int(p.y)
        grid[y][x] = p.color()

    # clear screen (FAST)
    print("\033[H\033[J", end="")

    # render grid
    for row in grid:
        print("".join(row))

    # stats
    print("\n" + "="*50)
    print("🧠 OMEGA QUANTUM FIELD v10.2 — PERSISTENT TRAILS")
    print("="*50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-"*50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Total Jumps  : {sum(p.jump for p in particles)}")
    print(f"🌈 Active Trails: {len(trails)}")
    print("="*50)

    print("\nKEY:")
    print("🟣🟢🔵⚪ = stable particle state")
    print("● (rainbow) = quantum return trail")

    sys.stdout.flush()


# =========================
# TRAIL DECAY
# =========================
def decay_trails():
    for t in trails:
        t["life"] -= 1

    trails[:] = [t for t in trails if t["life"] > 0]


# =========================
# MAIN LOOP (MANUAL ENGINE)
# =========================
try:
    while True:
        for p in particles:
            p.step()

        decay_trails()
        render()

        time.sleep(0.15)

except KeyboardInterrupt:
    print("\n🧠 Omega stopped safely.")
