import os
import time
import random

# -----------------------------
# CONFIG
# -----------------------------
SIZE = 40
NODES = 80
CACHE_TTL = 3.0

COLORS = ["🟣", "🟢", "🔵", "⚪"]

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

# -----------------------------
# SCAN CACHE (IMPORTANT FIX)
# -----------------------------
_SCAN_CACHE = {
    "time": 0,
    "data": (0, 0, 0)
}

def scan_files():
    global _SCAN_CACHE

    now = time.time()

    if now - _SCAN_CACHE["time"] < CACHE_TTL:
        return _SCAN_CACHE["data"]

    total = 0
    py = 0
    nodes = 0

    for path in OMEGA_PATHS:
        if not os.path.exists(path):
            continue

        for root, dirs, files in os.walk(path):
            for f in files:
                total += 1
                if f.endswith(".py"):
                    py += 1
                if "node" in f.lower():
                    nodes += 1

    result = (total, py, nodes)

    _SCAN_CACHE["time"] = now
    _SCAN_CACHE["data"] = result

    return result


# -----------------------------
# PARTICLE SYSTEM
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
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.vx = max(-1.5, min(1.5, self.vx))
        self.vy = max(-1.5, min(1.5, self.vy))

        # quantum jump event
        if random.random() < 0.12:
            self.jump += 1

    def color(self):
        # 🧠 deterministic + “quantum-like entropy”
        seed = (self.jump * 9973 + self.id * 31337) % 1000

        # IMPORTANT: jump triggers re-randomization phase
        if self.jump > 0 and seed % 7 == 0:
            return random.choice(COLORS)

        return COLORS[(seed // 10) % len(COLORS)]


# -----------------------------
# INIT
# -----------------------------
particles = [Particle(i) for i in range(NODES)]


# -----------------------------
# RENDER
# -----------------------------
def render():
    total, py, nodes = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    os.system("clear")

    for row in grid:
        print("".join(row))

    print("\n==============================")
    print("🧠 OMEGA v11 STABLE ENGINE")
    print("==============================")
    print(f"📦 Files   : {total}")
    print(f"🐍 Python  : {py}")
    print(f"🔗 Nodes   : {nodes}")
    print(f"🟣 Particles: {len(particles)}")
    print(f"⚡ Jumps   : {sum(p.jump for p in particles)}")
    print("==============================\n")


# -----------------------------
# MAIN LOOP (MANUAL CONTROL ONLY)
# -----------------------------
try:
    while True:
        for p in particles:
            p.step()

        render()
        time.sleep(0.08)

except KeyboardInterrupt:
    print("\n🧠 Omega stopped safely.")
