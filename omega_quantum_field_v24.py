import time
import random
import math

# ==================================================
# 🧠 OMEGA v24 — STRUCTURED FIELD ENGINE
# ==================================================

SIZE = 40
NUM_PARTICLES = 60

FIELD = {
    "entropy": 0.5,
    "pressure": 1.0,
    "coupling": 0.08
}

particles = []
trails = []
attractors = []


# ==================================================
# 🧠 PARTICLE MODEL
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.history = []

    def influence(self, others):
        for o in others:
            if o is self:
                continue

            dx = o.x - self.x
            dy = o.y - self.y

            dist = max(1, math.sqrt(dx*dx + dy*dy))

            if dist < 8:
                weight = len(o.history) * 0.01
                force = FIELD["coupling"] * weight

                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force


    def apply_attractors(self):
        for a in attractors:
            dx = a["x"] - self.x
            dy = a["y"] - self.y

            dist = max(1, math.sqrt(dx*dx + dy*dy))

            if dist < 14:
                force = a["strength"] / dist
                self.vx += dx * force * 0.01
                self.vy += dy * force * 0.01


    def step(self, others):
        self.history.append((self.x, self.y))
        if len(self.history) > 5:
            self.history.pop(0)

        self.influence(others)
        self.apply_attractors()

        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        self.vx *= 0.96
        self.vy *= 0.96


# ==================================================
# 🧠 FIELD EVOLUTION
# ==================================================
def update_field():
    FIELD["entropy"] *= 0.995

    if random.random() > 0.85:
        attractors.append({
            "x": random.randint(0, SIZE - 1),
            "y": random.randint(0, SIZE - 1),
            "strength": random.random()
        })

    if len(attractors) > 12:
        attractors.pop(0)


# ==================================================
# 🧠 MEMORY SYSTEM
# ==================================================
def record(p):
    trails.append({"x": p.x, "y": p.y, "s": "·"})


def decay():
    if len(trails) > 500:
        del trails[:120]


# ==================================================
# 🧠 RENDER ENGINE (RESTORED VISUAL HIERARCHY)
# ==================================================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # 🟣 LAYER 1: attractors (always visible)
    for a in attractors:
        grid[a["y"]][a["x"]] = "🟣"

    # ● LAYER 2: particles (filtered clarity layer)
    for i, p in enumerate(particles):
        if i % 2 == 0:
            grid[p.y][p.x] = "●"

    # · LAYER 3: memory (sparse field projection)
    for i, t in enumerate(trails[-400:]):
        if i % 3 == 0:
            grid[t["y"]][t["x"]] = "·"

    print("\n🧠 OMEGA v24 — STRUCTURED FIELD ENGINE")
    print(f"particles={len(particles)} trails={len(trails)} attractors={len(attractors)}")
    print(f"coupling={FIELD["coupling"]:.3f} entropy={FIELD["entropy"]:.3f}")

    for row in grid:
        print("".join(row))

    # 1. attractors (top layer)
    for a in attractors:
        grid[a["y"]][a["x"]] = "🟣"

    # 2. particles
    for p in particles:
        grid[p.y][p.x] = "●"

        # memory ghosts (low opacity)
        for hx, hy in p.history:
            if random.random() > 0.9:
                grid[hy][hx] = "·"

    # 3. trails (background)
    for t in trails[-600:]:
        grid[t["y"]][t["x"]] = t["s"]

    print("\n🧠 OMEGA v24 — STRUCTURED FIELD ENGINE")
    print(f"particles={len(particles)} trails={len(trails)} attractors={len(attractors)}")
    print(f"coupling={FIELD['coupling']:.3f} entropy={FIELD['entropy']:.3f}")

    for row in grid:
        print("".join(row))


# ==================================================
# 🧠 INIT
# ==================================================
for _ in range(NUM_PARTICLES):
    particles.append(Particle())


# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:
        for p in particles:
            p.step(particles)
            record(p)

        update_field()
        decay()
        render()

        time.sleep(0.18)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v24 STOPPED SAFELY")
