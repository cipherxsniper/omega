import os
import time
import random
import math

SIZE = 40
PARTICLES = 60

FIELD = {
    "pressure": 0.0,
    "entropy": 0.0
}

base_colors = ["🟣","🟢","🔵","⚪"]

def particle_color(p):
    return base_colors[int(p.x + p.y) % len(base_colors)]

heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def update_heat(x, y):
    heatmap[y][x] += 2

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= 0.95

trails = []

def add_trail(x, y):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "color": "✦" if random.random() < 0.5 else "●"
    })

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

# =========================
# PARTICLE (INTERACTION UPGRADED)
# =========================
class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def interact(self, others):
        # LOCAL GRAVITY / REPULSION
        for o in others:
            if o is self:
                continue

            dx = o.x - self.x
            dy = o.y - self.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.001

            # attraction if close, repulsion if too close
            if dist < 6:
                force = 0.02
                self.vx += dx / dist * force
                self.vy += dy / dist * force

            if dist < 2:
                self.vx -= dx / dist * 0.05
                self.vy -= dy / dist * 0.05

    def step(self, others):

        self.interact(others)

        # field influence
        self.vx += FIELD["entropy"] * 0.01
        self.vy += FIELD["pressure"] * 0.01

        # motion
        self.x += self.vx
        self.y += self.vy

        # bounds
        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        # trail memory
        if random.random() < 0.06:
            add_trail(int(self.x), int(self.y))

        if abs(self.vx) > 0.4 or abs(self.vy) > 0.4:
            add_trail(int(self.x), int(self.y))

particles = [Particle() for _ in range(PARTICLES)]

# =========================
# FIELD UPDATE
# =========================
def update_field():
    FIELD["pressure"] = sum(p.vx**2 + p.vy**2 for p in particles) * 0.01
    FIELD["entropy"] = random.random()

# =========================
# RENDER
# =========================
def render():

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # HEAT
    for y in range(SIZE):
        for x in range(SIZE):
            v = heatmap[y][x]
            if v > 30: grid[y][x] = "🟥"
            elif v > 20: grid[y][x] = "🟧"
            elif v > 10: grid[y][x] = "🟨"
            elif v > 5: grid[y][x] = "🟩"

    # TRAILS
    for t in trails:
        grid[t["y"]][t["x"]] = t["color"]

    # PARTICLES
    for p in particles:
        grid[int(p.y)][int(p.x)] = particle_color(p)

    print("\033[H\033[J", end="")
    for row in grid:
        print("".join(row))

    print("\n🧠 OMEGA v15.2 — INTERACTION FIELD")

# =========================
# MAIN LOOP
# =========================
try:
    while True:

        update_field()

        for p in particles:
            p.step(particles)

        decay_trails()
        decay_heat()

        render()

        time.sleep(0.12)

except KeyboardInterrupt:
    print("STOPPED")
