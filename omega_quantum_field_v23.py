import time
import random
import math

# ==================================================
# 🧠 OMEGA v23 — MULTI-AGENT INTERACTION FIELD
# ==================================================

SIZE = 40
NUM_PARTICLES = 60

FIELD = {
    "entropy": 0.5,
    "pressure": 1.0,
    "coupling": 0.08   # v23: interaction strength
}

particles = []
trails = []
attractors = []


# ==================================================
# 🧠 PARTICLE (MULTI-AGENT NODE)
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.history = []

    def influence(self, others):
        """v23: particle-to-particle memory coupling"""

        for o in others:
            if o is self:
                continue

            dx = o.x - self.x
            dy = o.y - self.y

            dist = max(1, math.sqrt(dx*dx + dy*dy))

            # local interaction radius
            if dist < 8:

                # memory field coupling
                memory_weight = len(o.history) * 0.01

                force = FIELD["coupling"] * memory_weight

                self.vx += (dx / dist) * force
                self.vy += (dy / dist) * force


    def step(self, others):
        # store memory
        self.history.append((self.x, self.y))
        if len(self.history) > 5:
            self.history.pop(0)

        # multi-agent influence FIRST
        self.influence(others)

        # movement
        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        # damping
        self.vx *= 0.96
        self.vy *= 0.96


# ==================================================
# 🧠 FIELD EVOLUTION
# ==================================================
def update_field():
    FIELD["entropy"] *= 0.995
    FIELD["pressure"] = 1.0 + random.random() * 0.15

    # emergent attractors
    if random.random() > 0.85:
        attractors.append({
            "x": random.randint(0, SIZE - 1),
            "y": random.randint(0, SIZE - 1),
            "strength": random.random()
        })

    if len(attractors) > 12:
        attractors.pop(0)


# ==================================================
# 🧠 TRAILS
# ==================================================
def record(p):
    trails.append({"x": p.x, "y": p.y, "s": "✦"})


def decay():
    if len(trails) > 900:
        del trails[:200]


# ==================================================
# 🧠 RENDER ENGINE (v11 + v22 + v23)
# ==================================================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # trails
    for t in trails[-700:]:
        grid[t["y"]][t["x"]] = t["s"]

    # particles
    for p in particles:
        grid[p.y][p.x] = "●"

        # memory ghosting
        for hx, hy in p.history:
            if random.random() > 0.7:
                grid[hy][hx] = "·"

    # attractors
    for a in attractors:
        grid[a["y"]][a["x"]] = "🟣"

    print("\n🧠 OMEGA v23 — MULTI-AGENT INTERACTION FIELD")
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
# 🔁 LOOP
# ==================================================
try:
    while True:

        # step with full swarm awareness
        for p in particles:
            p.step(particles)
            record(p)

        update_field()
        decay()
        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v23 STOPPED SAFELY")
