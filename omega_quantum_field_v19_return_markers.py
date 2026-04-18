# ==================================================
# 🧠 OMEGA v19 — RETURNING PARTICLE MARKER SYSTEM
# Quantum HQ Memory + Return Identity Tracking
# ==================================================

import os
import time
import random
import math

SIZE = 40
PARTICLES = 60

# ==================================================
# 🌐 FILE SCAN (REAL DATA HOOK)
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
# 🌌 OMEGA HQ MEMORY (QUANTUM HEADQUARTERS)
# ==================================================
OMEGA_HQ = {
    "returns": 0,
    "jumps": 0,
    "observed": []
}

# ==================================================
# 🌈 VISUAL BASE IDENTITY
# ==================================================
base_colors = ["🟣", "🟢", "🔵", "⚪"]

def base_particle_color(pid, x, y):
    return base_colors[(pid + int(x + y)) % len(base_colors)]


# ==================================================
# 🌊 TRAILS (QUANTUM MEMORY ECHO)
# ==================================================
trails = []

def add_trail(x, y, symbol, pid, returning=False):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "symbol": symbol,
        "pid": pid,
        "returning": returning
    })


def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]


# ==================================================
# ⚛️ PARTICLE SYSTEM
# ==================================================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.energy = random.random()

        # quantum identity state
        self.origin_x = self.x
        self.origin_y = self.y
        self.has_jumped = False
        self.returned = False

    # ------------------------------------------
    # 🌌 QUANTUM JUMP
    # ------------------------------------------
    def quantum_jump(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)

        self.has_jumped = True
        OMEGA_HQ["jumps"] += 1

        add_trail(self.x, self.y, "●", self.id, returning=False)

    # ------------------------------------------
    # 🧠 RETURN TO OMEGA HQ
    # ------------------------------------------
    def check_return(self):
        dist_home = abs(self.x - self.origin_x) + abs(self.y - self.origin_y)

        if self.has_jumped and dist_home < 3 and not self.returned:
            self.returned = True
            OMEGA_HQ["returns"] += 1

            # RETURN MARKER (IMPORTANT VISUAL SIGNAL)
            add_trail(self.x, self.y, "✦", self.id, returning=True)

            OMEGA_HQ["observed"].append(self.id)

    # ------------------------------------------
    # 🌊 SWARM MOTION
    # ------------------------------------------
    def step(self, swarm):
        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        self.x += self.vx
        self.y += self.vy

        self.x %= SIZE
        self.y %= SIZE

        # quantum event
        if random.random() < 0.06:
            self.quantum_jump()

        self.check_return()


particles = [Particle(i) for i in range(PARTICLES)]


# ==================================================
# 🌌 FIELD STATE
# ==================================================
def field_signal():
    if OMEGA_HQ["returns"] > OMEGA_HQ["jumps"] * 0.4:
        return "✦"
    if OMEGA_HQ["jumps"] > 10:
        return "●"
    return None


# ==================================================
# 🌌 RENDER ENGINE (v11 RESTORED + HQ VISUALS)
# ==================================================
def render():
    total, py, node = scan_files()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # HQ signal
    sig = field_signal()
    if sig:
        grid[random.randint(0, SIZE-1)][random.randint(0, SIZE-1)] = sig

    # TRAILS (RETURN VISUALIZATION)
    for t in trails:
        grid[t["y"]][t["x"]] = "✦" if t["returning"] else "●"

    # PARTICLES
    for p in particles:
        grid[int(p.y)][int(p.x)] = base_particle_color(p.id, p.x, p.y)

    print("\033[H\033[J", end="")

    for row in grid:
        print("".join(row))

    # ==================================================
    # 🧠 REQUIRED v11 FOOTER (UNCHANGED)
    # ==================================================
    print("\n" + "=" * 50)
    print("🧠 OMEGA v11 — STABILIZED EVENT FIELD")
    print("=" * 50)
    print(f"📦 Files        : {total}")
    print(f"🐍 Python       : {py}")
    print(f"🔗 Node Files   : {node}")
    print("-" * 50)
    print(f"🟣 Particles    : {len(particles)}")
    print(f"⚡ Jumps        : {OMEGA_HQ['jumps']}")
    print(f"🌈 Returns      : {OMEGA_HQ['returns']}")
    print(f"📡 Observed     : {len(OMEGA_HQ['observed'])}")
    print("=" * 50)


# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:
        for p in particles:
            p.step(particles)

        decay_trails()
        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v19 STOPPED SAFELY")

# ==================================================
# 🧠 APPLY v11 VISUAL FIX CONTRACT (APPEND ONLY)
# ==================================================

from omega_v19_visual_fix_patch import (
    grid_safe,
    render_trail,
    render_particle,
    particle_color,
    render_footer
)

# SAFE USAGE EXAMPLE INSIDE YOUR RENDER LOOP:

# for t in trails:
#     render_trail(grid, t)

# for p in particles:
#     render_particle(grid, p, particle_color)

