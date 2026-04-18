import time
import random

# ==================================================
# 🧠 FIELD STATE
# ==================================================
FIELD = {
    "entropy": 0.55,
    "pressure": 1.0,
    "awareness": 0.0,
}

SIZE = 40

particles = []
trails = []
attractors = []
MEMORY = {"validated_packets": 0, "rejected_packets": 0}


# ==================================================
# 🧠 PARTICLE SYSTEM
# ==================================================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.energy = random.random()

    def step(self):
        self.x = (self.x + int(self.vx)) % SIZE
        self.y = (self.y + int(self.vy)) % SIZE

        self.vx *= 0.97
        self.vy *= 0.97

        # awareness drift
        self.energy *= 0.999


# ==================================================
# 🧠 FIELD FUNCTIONS
# ==================================================
def update_field():
    FIELD["entropy"] *= 0.995
    FIELD["pressure"] = 1.0 + random.random() * 0.2
    FIELD["awareness"] = min(1.0, FIELD["awareness"] + 0.002)


def decay_trails():
    if len(trails) > 800:
        del trails[:200]


def spawn_attractor():
    if len(attractors) < 10 and random.random() < 0.1:
        attractors.append({
            "x": random.randint(0, SIZE - 1),
            "y": random.randint(0, SIZE - 1),
            "power": random.random() + 0.5
        })


def galaxy_influence(p):
    for a in attractors:
        dx = a["x"] - p.x
        dy = a["y"] - p.y
        p.vx += dx * 0.0005 * a["power"]
        p.vy += dy * 0.0005 * a["power"]


def register_observation(x, y):
    trails.append({"x": x, "y": y, "symbol": "✦"})


def field_symbol():
    if FIELD["entropy"] > 0.6:
        return "✦"
    if FIELD["pressure"] > 1.5:
        return "●"
    return None


# ==================================================
# 🧠 VISUAL RENDER (OMEGA V11 STYLE FIELD GRID)
# ==================================================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # field noise
    sym = field_symbol()
    if sym:
        for _ in range(5):
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            grid[y][x] = sym

    # trails
    for t in trails:
        grid[t["y"]][t["x"]] = t["symbol"]

    # attractors
    for a in attractors:
        grid[a["y"]][a["x"]] = "🟣"

    print("\n".join("".join(row) for row in grid))

    print("\n==================================================")
    print("🧠 OMEGA v18 — FIELD VISUAL CORE")
    print("==================================================")
    print(f"particles={len(particles)} trails={len(trails)} attractors={len(attractors)}")
    print(f"entropy={FIELD['entropy']:.3f} awareness={FIELD['awareness']:.3f}")
    print("==================================================\n")


# ==================================================
# 🧠 INIT
# ==================================================
for _ in range(60):
    particles.append(Particle())


# ==================================================
# 🔁 MAIN LOOP
# ==================================================
try:
    while True:

        spawn_attractor()

        for p in particles:
            p.step()
            galaxy_influence(p)
            register_observation(p.x, p.y)

        update_field()
        decay_trails()

        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 OMEGA v18 STOPPED SAFELY")
