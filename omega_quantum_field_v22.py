import time
import random
import math

# ==================================================
# 🧠 OMEGA v22 — TEMPORAL FIELD MEMORY SYSTEM
# ==================================================

SIZE = 40

FIELD = {
    "entropy": 0.5,
    "pressure": 1.0,
    "observer": 1.0
}

particles = []
trails = []
attractors = []

# ==================================================
# 🧠 PARTICLE WITH MEMORY
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        # v22: memory trail inside particle
        self.history = []

    def step(self):
        # store memory
        self.history.append((self.x, self.y))
        if len(self.history) > 6:
            self.history.pop(0)

        # movement
        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        # memory gravity (pull toward past self positions)
        for hx, hy in self.history:
            dx = hx - self.x
            dy = hy - self.y
            self.vx += dx * 0.001
            self.vy += dy * 0.001

        self.vx *= 0.97
        self.vy *= 0.97


# ==================================================
# 🧠 FIELD EVOLUTION
# ==================================================
def update_field():
    FIELD["entropy"] *= 0.995
    FIELD["pressure"] = 1.0 + random.random() * 0.15

    # attractor evolution (self-growing structure)
    if random.random() > 0.82:
        attractors.append({
            "x": random.randint(0, SIZE - 1),
            "y": random.randint(0, SIZE - 1),
            "strength": random.random()
        })

    if len(attractors) > 14:
        attractors.pop(0)


# ==================================================
# 🧠 TRAIL SYSTEM
# ==================================================
def record(p):
    trails.append({"x": p.x, "y": p.y, "s": "✦"})


def decay():
    if len(trails) > 900:
        del trails[:200]


# ==================================================
# 🧠 RENDER ENGINE (v11 restored + v22 enhancement)
# ==================================================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # trails
    for t in trails[-700:]:
        grid[t["y"]][t["x"]] = t["s"]

    # particles
    for p in particles:
        grid[p.y][p.x] = "●"

        # memory ghost (faint past positions)
        for hx, hy in p.history:
            if random.random() > 0.6:
                grid[hy][hx] = "·"

    # attractors (hidden structure visible only in render phase)
    for a in attractors:
        if random.random() > 0.4:
            grid[a["y"]][a["x"]] = "🟣"

    print("\n🧠 OMEGA v22 — TEMPORAL FIELD SYSTEM")
    print(f"particles={len(particles)} trails={len(trails)} attractors={len(attractors)}")
    print(f"entropy={FIELD['entropy']:.3f} observer={FIELD['observer']:.3f}")

    for row in grid:
        print("".join(row))


# ==================================================
# 🧠 INIT
# ==================================================
for _ in range(60):
    particles.append(Particle())


# ==================================================
# 🔁 LOOP
# ==================================================
try:
    while True:
        for p in particles:
            p.step()
            record(p)

        update_field()
        decay()
        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v22 STOPPED SAFELY")
