import time
import random
import math

# ==================================================
# 🧠 FIELD STATE
# ==================================================
FIELD = {
    "entropy": 0.5,
    "pressure": 1.0,
}

SIZE = 40
particles = []
trails = []

MEMORY = {
    "dark_matter": 31,
    "hidden": 19,
    "attractors": []
}

# ==================================================
# 🧠 PARTICLE
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def step(self):
        # normal motion
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        # DARK MATTER GRAVITY (hidden pull)
        for a in MEMORY["attractors"]:
            dx = a["x"] - self.x
            dy = a["y"] - self.y
            dist = max(1, math.sqrt(dx*dx + dy*dy))

            self.vx += (dx / dist) * 0.01
            self.vy += (dy / dist) * 0.01

        self.vx *= 0.98
        self.vy *= 0.98


# ==================================================
# 🧠 DARK MATTER FIELD GENERATION
# ==================================================
def update_dark_field():
    if random.random() < 0.15:
        MEMORY["attractors"].append({
            "x": random.randint(0, SIZE-1),
            "y": random.randint(0, SIZE-1),
            "strength": random.random()
        })

    # decay hidden structure
    if len(MEMORY["attractors"]) > 12:
        MEMORY["attractors"].pop(0)


def update_field():
    FIELD["entropy"] *= 0.99
    FIELD["pressure"] = 1.0 + random.random() * 0.2


def decay_trails():
    if len(trails) > 500:
        del trails[:100]


def register_observation(x, y):
    trails.append({"x": x, "y": y, "symbol": "✦"})


def render():
    print("🧠 OMEGA v19 — DARK MATTER FIELD SYSTEM")
    print(f"particles={len(particles)} trails={len(trails)}")
    print(f"visible attractors={len(MEMORY['attractors'])}")
    print(f"dark matter={MEMORY['dark_matter']} hidden={MEMORY['hidden']}")
    print(f"awareness={FIELD['entropy']:.3f}")
    print("="*50)


# ==================================================
# 🧠 INIT
# ==================================================
for _ in range(60):
    particles.append(Particle())

# ==================================================
# 🧠 LOOP
# ==================================================
try:
    while True:
        update_dark_field()

        for p in particles:
            p.step()
            register_observation(p.x, p.y)

        update_field()
        decay_trails()
        render()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🧠 OMEGA v19 STOPPED SAFELY")
