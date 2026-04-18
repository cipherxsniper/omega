from omega_conscious_field_v20 import step_conscious_field, register_observation
from omega_dark_matter_v19 import step_dark_matter_system
from omega_galaxy_memory_v17 import step_galaxy_system, galaxy_influence
from omega_galaxy_system_v17 import update_galaxies, galaxies, Galaxy
# ==================================================
# 🧠 OMEGA v17 — FUSED LIVING INTELLIGENCE FIELD
# v11 VISUAL LIFE + v13 IDENTITY + VALIDATION LAYER
# ==================================================

import os
import time
import random
import math

SIZE = 40
PARTICLES = 60

# ==================================================
# 🌐 FILE / NODE SCAN (OMEGA REALITY LAYER)
# ==================================================
def scan_files():
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

    return total, py, node


# ==================================================
# 🌌 FIELD STATE (GLOBAL MIND WEATHER)
# ==================================================
FIELD = {
    "pressure": 0.0,
    "coherence": 0.0,
    "entropy": 0.0
}

# ==================================================
# 🧠 MEMORY (VALIDATION LAYER)
# ==================================================
MEMORY = {
    "validated_packets": 0,
    "rejected_packets": 0,
    "sync_count": 0
}

# ==================================================
# 🌊 VISUAL SYSTEMS (v11 RESTORED FEEL)
# ==================================================
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def particle_color(p):
    return base_colors[(int(p.x + p.y)) % len(base_colors)]


def rainbow():
    return random.choice(["✦", "●"])


# ==================================================
# 🌱 TRAILS (QUANTUM JUMP HISTORY)
# ==================================================
trails = []

def add_trail(x, y):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "symbol": rainbow()
    })


def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# ==================================================
# 🧠 VALIDATOR PARTICLE (NEW SYSTEM CORE)
# ==================================================
class Validator:
    def validate(self, particle):
        # simple but powerful rule: coherence decides truth
        score = random.random()

        if score > 0.6:
            MEMORY["validated_packets"] += 1
            return True
        else:
            MEMORY["rejected_packets"] += 1
            return False


validator = Validator()


# ==================================================
# ⚛️ PARTICLE SYSTEM (DATA + MOTION + IDENTITY)
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.jump = 0

    def step(self):
        # movement
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        self.x %= SIZE
        self.y %= SIZE

        # v11 STYLE VISUAL TRAIL TRIGGER
        if abs(self.vx) > 0.3 or abs(self.vy) > 0.3:
            add_trail(int(self.x), int(self.y))

        # quantum jump
        if random.random() < 0.06:
            self.jump += 1
            add_trail(int(self.x), int(self.y))

        # validation event
        if validator.validate(self):
            FIELD["coherence"] += 0.001
        else:
            FIELD["entropy"] += 0.001


particles = [Particle() for _ in range(PARTICLES)]


# ==================================================
# 🌌 FIELD UPDATE (GLOBAL BEHAVIOR LOOP)
# ==================================================
def update_field():
    FIELD["pressure"] = len(trails) * 0.1
# ==================================================

# 🧠 RENDER (v11 VISUAL RESTORATION CORE)

# ==================================================

def render():

    total, py, node = scan_files()



    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]



    # heat field

    sym = field_symbol()

    if sym:

        fx = random.randint(0, SIZE - 1)

        fy = random.randint(0, SIZE - 1)

        grid[fy][fx] = sym



    # trails FIRST (memory layer)

    for t in trails:

        if 0 <= t["x"] < SIZE and 0 <= t["y"] < SIZE:

            grid[t["y"]][t["x"]] = t["symbol"]



    # particles (core life)
    for p in particles:
        grid[int(p.y)][int(p.x)] = particle_color(p)

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    # ==================================================
# ==================================================

# 🔁 MAIN LOOP (OMEGA CONTINUOUS FIELD)

# ==================================================

try:

    while True:

        for p in particles:

            try:

                p.step()

                galaxy_influence(p)

            except Exception:

                pass



        update_field()

        decay_trails()



