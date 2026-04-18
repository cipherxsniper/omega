import os
import time
import random
import sys
import math

SIZE = 40
PARTICLES = 60

# =========================
# 🌈 SPARK FIELD (v11 RESTORE)
# =========================
RAINBOW = ["🟥","🟧","🟨","🟩","🟦","🟪","⚪"]
sparks = []

def emit_spark(x, y):
    if random.random() < 0.08:
        sparks.append({
            "x": x,
            "y": y,
            "color": random.choice(RAINBOW),
            "life": random.randint(2, 5)
        })

def decay_sparks():
    for s in sparks:
        s["life"] -= 1
    sparks[:] = [s for s in sparks if s["life"] > 0]

# =========================
# 🌡️ HEAT + MEMORY FIELD
# =========================
heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

def update_heat(x, y):
    heatmap[y][x] += 1

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= 0.97

# =========================
# 🧠 SWARM MEMORY FIELD (GLOBAL COGNITION)
# =========================
swarm_memory = {
    "avg_vx": 0,
    "avg_vy": 0
}

# =========================
# 📡 EVENTS
# =========================
events = []

def emit_event(x, y, strength):
    events.append({
        "x": x,
        "y": y,
        "strength": strength,
        "life": 8
    })

def decay_events():
    for e in events:
        e["life"] -= 1
        e["strength"] *= 0.88
    events[:] = [e for e in events if e["life"] > 0]

# =========================
# 🧠 PARTICLE SYSTEM (v15 CORE)
# =========================
class Particle:
    def __init__(self, i):
        self.id = i
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.memory = []

    def field_entropy(self):
        heat = heatmap[int(self.y)][int(self.x)]
        return (
            math.sin(self.x * 12.9898 + self.y * 78.233) * 43758.5453 % 1 +
            (self.vx * self.vy) * 0.01 +
            heat * 0.0001
        )

    def step(self):
        q = self.field_entropy()

        # =========================
        # EVENT FORCE
        # =========================
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y
            d = math.sqrt(dx*dx + dy*dy) + 0.1

            influence = e["strength"] / d
            self.vx += (dx/d) * influence * 0.05
            self.vy += (dy/d) * influence * 0.05

        # =========================
        # SWARM MEMORY INJECTION
        # =========================
        self.vx += swarm_memory["avg_vx"] * 0.02
        self.vy += swarm_memory["avg_vy"] * 0.02

        # =========================
        # LOCAL SWARM COHESION
        # =========================
        for p in particles:
            if p is not self:
                dx = p.x - self.x
                dy = p.y - self.y
                d = math.sqrt(dx*dx + dy*dy) + 0.1

                if d < 6:
                    self.vx += dx / d * 0.01
                    self.vy += dy / d * 0.01

        # =========================
        # MEMORY (TRAJECTORY LEARNING)
        # =========================
        self.memory.append((self.vx, self.vy))
        if len(self.memory) > 5:
            self.memory.pop(0)

        mem_vx = sum(m[0] for m in self.memory) / len(self.memory)
        mem_vy = sum(m[1] for m in self.memory) / len(self.memory)

        # =========================
        # QUANTUM DRIFT
        # =========================
        self.vx += q * 0.2 + mem_vx * 0.05
        self.vy += q * 0.2 + mem_vy * 0.05

        # =========================
        # POSITION UPDATE
        # =========================
        self.x += self.vx
        self.y += self.vy

        self.vx += random.uniform(-0.1, 0.1)
        self.vy += random.uniform(-0.1, 0.1)

        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 1.6:
            self.vx *= 0.8
            self.vy *= 0.8

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        # =========================
        # SPARK EMISSION (v11 RESTORE)
        # =========================
        emit_spark(int(self.x), int(self.y))

        # =========================
        # EVENT EMISSION
        # =========================
        if random.random() < 0.06 + q:
            emit_event(int(self.x), int(self.y), 0.8 + q)

        # update swarm memory
        swarm_memory["avg_vx"] = (swarm_memory["avg_vx"] + self.vx) * 0.5
        swarm_memory["avg_vy"] = (swarm_memory["avg_vy"] + self.vy) * 0.5

    def color(self):
        base = ["🟣","🟢","🔵","⚪"]
        return base[int(abs(self.vx + self.vy)) % 4]

particles = [Particle(i) for i in range(PARTICLES)]

# =========================
# RENDER SYSTEM
# =========================
def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # SPARK LAYER
    for s in sparks:
        if 0 <= s["x"] < SIZE and 0 <= s["y"] < SIZE:
            grid[s["y"]][s["x"]] = s["color"]

    # EVENT LAYER
    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    # PARTICLE LAYER
    for p in particles:
        grid[int(p.y)][int(p.x)] = p.color()

    print("\033[H\033[J", end="")
    for row in grid:
        print("".join(row))

    print("\n🧠 OMEGA v15 — HYBRID FIELD")

# =========================
# MAIN LOOP
# =========================
try:
    while True:
        for p in particles:
            p.step()

        decay_sparks()
        decay_events()
        decay_heat()

        render()
        time.sleep(0.12)

except KeyboardInterrupt:
    print("\n🧠 Omega stopped safely.")

# ORBITAL SYSTEM UPDATE (v17)
step_orbit_system(particles)


# ORBITAL ATTRACTOR SEEDING (v17)
maybe_create_attractor(int(e['x']), int(e['y']), e['strength'])

