import time
import random
from collections import defaultdict

# ==================================================
# 🧠 OMEGA v26 — UNIFIED VISUAL SWARM ENGINE
# ==================================================

SIZE = 40
NUM_PARTICLES = 60

FIELD = {
    "entropy": 0.5,
    "pressure": 1.0,
    "observer": 1.0
}

particles = []
bonds = set()
molecules = defaultdict(list)
hidden_attractors = []

# ==================================================
# 🧠 PARTICLE
# ==================================================

class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.id = id(self)

    def move(self):
        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        # v23 swarm coupling
        self.vx += random.uniform(-0.05, 0.05)
        self.vy += random.uniform(-0.05, 0.05)

        # damping
        self.vx *= 0.98
        self.vy *= 0.98

# ==================================================
# 🧠 INITIALIZE
# ==================================================

for _ in range(NUM_PARTICLES):
    particles.append(Particle())

# ==================================================
# 🧠 PHYSICS
# ==================================================

def update_physics():
    FIELD["entropy"] *= 0.995
    FIELD["pressure"] = 1.0 + random.random() * 0.1

def rebuild_molecules():
    molecules.clear()
    bonds.clear()

    for i, a in enumerate(particles):
        for j, b in enumerate(particles):
            if i >= j:
                continue

            dist = abs(a.x - b.x) + abs(a.y - b.y)

            if dist < 3 + random.randint(0, 1):
                bonds.add((i, j))

                # molecular grouping
                molecules[i].append(j)

def update_hidden_attractors():
    hidden_attractors.clear()
    if FIELD["entropy"] < 0.3:
        for _ in range(3):
            hidden_attractors.append(
                (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
            )

# ==================================================
# 🧠 RENDER (v11 STYLE RESTORED + LIVE STATE)
# ==================================================

def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # hidden attractors (v19)
    for ax, ay in hidden_attractors:
        grid[ay][ax] = "🟢"

    # particles (v20 observer + v11 visual)
    for p in particles:
        symbol = "✦" if random.random() < FIELD["observer"] else "●"
        grid[p.y][p.x] = symbol

    print("\n🧠 OMEGA v26 — UNIFIED VISUAL SWARM ENGINE")
    print(f"particles={len(particles)} bonds={len(bonds)} entropy={FIELD['entropy']:.3f}")

    for row in grid:
        print("".join(row))

# ==================================================
# 🧠 MAIN LOOP (STATE DRIVEN RENDER)
# ==================================================

try:
    while True:

        # 1. move physics FIRST
        for p in particles:
            p.move()

        # 2. update field
        update_physics()

        # 3. rebuild EVERYTHING from CURRENT state
        rebuild_molecules()
        update_hidden_attractors()

        # 4. render ONLY current state (no stored visuals)
        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v26 STOPPED SAFELY")
