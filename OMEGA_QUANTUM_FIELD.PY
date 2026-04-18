# ================================
# OMEGA v12 — PARTICLE MEMORY FIELD SYSTEM
# PMF-IS (Particle Memory Field Intelligence System)
# ================================

import os
import time
import random
import math
import sys

# ================================
# CONFIG
# ================================
SIZE = 40
INITIAL_PARTICLES = 60
MAX_PARTICLES = 220
TICK_RATE = 0.12

HEAT_DECAY = 0.97
EVENT_DECAY = 0.90

REPLICATION_THRESHOLD = 6.0
JUMP_CHANCE = 0.06

# ================================
# MEMORY FIELDS
# ================================
heatmap = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
events = []
trails = []

# ================================
# UTILS
# ================================
def clear():
    print("\033[H\033[J", end="")

def clamp(v, mn, mx):
    return max(mn, min(mx, v))

def rand_color():
    return random.choice([
        "\033[95m", "\033[94m", "\033[96m",
        "\033[92m", "\033[93m", "\033[91m"
    ]) + "●\033[0m"

# ================================
# EVENT SYSTEM (GRAVITY NODES)
# ================================
def emit_event(x, y, strength):
    events.append({
        "x": x,
        "y": y,
        "strength": strength,
        "life": 10
    })

def decay_events():
    global events
    for e in events:
        e["life"] -= 1
        e["strength"] *= EVENT_DECAY
    events = [e for e in events if e["life"] > 0]

# ================================
# HEAT FIELD (MEMORY IMPRINT)
# ================================
def heat(x, y):
    heatmap[y][x] += 1

def decay_heat():
    for y in range(SIZE):
        for x in range(SIZE):
            heatmap[y][x] *= HEAT_DECAY

# ================================
# PARTICLE AGENT (CORE INTELLIGENCE UNIT)
# ================================
class Particle:
    def __init__(self, pid):
        self.id = pid
        self.x = random.randint(0, SIZE - 1)
        self.y = random.randint(0, SIZE - 1)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.energy = 1.0
        self.reward = 0.0
        self.jump = 0
        self.memory = []

    # ----------------------------
    # CORE DECISION SYSTEM
    # ----------------------------
    def step(self):
        global particles

        # EVENT GRAVITY INFLUENCE
        for e in events:
            dx = e["x"] - self.x
            dy = e["y"] - self.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1

            force = e["strength"] / dist

            self.vx += (dx / dist) * force * 0.04
            self.vy += (dy / dist) * force * 0.04

            self.reward += force * 0.1

        # RANDOM ENTROPY
        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        # SPEED LIMIT
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > 1.6:
            self.vx *= 0.7
            self.vy *= 0.7

        # MOVE
        self.x = (self.x + self.vx) % SIZE
        self.y = (self.y + self.vy) % SIZE

        ix, iy = int(self.x), int(self.y)

        # MEMORY FORMATION
        heat(ix, iy)
        self.memory.append((ix, iy))

        # EVENT EMISSION
        if random.random() < JUMP_CHANCE:
            self.jump += 1
            emit_event(ix, iy, random.uniform(0.5, 2.5))

        # TRAIL EMISSION
        if random.random() < 0.03:
            trails.append({
                "x": ix,
                "y": iy,
                "life": random.randint(3, 6),
                "color": rand_color()
            })

        # REPLICATION LOGIC (KEY UPGRADE)
        if self.reward > REPLICATION_THRESHOLD and len(particles) < MAX_PARTICLES:
            self.reward *= 0.4

            clone = Particle(len(particles))
            clone.x, clone.y = self.x, self.y
            clone.vx = self.vx + random.uniform(-0.3, 0.3)
            clone.vy = self.vy + random.uniform(-0.3, 0.3)

            particles.append(clone)

    # ----------------------------
    # VISUAL STATE
    # ----------------------------
    def symbol(self):
        base = ["🟣", "🔵", "🟢", "⚪"]
        return base[self.jump % len(base)]

# ================================
# SYSTEM INITIALIZATION
# ================================
particles = [Particle(i) for i in range(INITIAL_PARTICLES)]

# ================================
# DECAY SYSTEMS
# ================================
def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

# ================================
# RENDER ENGINE (OMEGA DASHBOARD)
# ================================
def render():
    clear()

    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    # HEAT LAYER
    for y in range(SIZE):
        for x in range(SIZE):
            v = heatmap[y][x]
            if v > 20:
                grid[y][x] = "🟥"
            elif v > 12:
                grid[y][x] = "🟧"
            elif v > 6:
                grid[y][x] = "🟨"
            elif v > 2:
                grid[y][x] = "🟩"

    # EVENT LAYER
    for e in events:
        grid[int(e["y"])][int(e["x"])] = "✦"

    # TRAILS
    for t in trails:
        grid[t["y"]][t["x"]] = t["color"]

    # PARTICLES
    for p in particles:
        grid[int(p.y)][int(p.x)] = p.symbol()

    # DISPLAY GRID
    for row in grid:
        print("".join(row))

    # ================================
    # DASHBOARD PANEL
    # ================================
    total_heat = sum(sum(row) for row in heatmap)

    print("\n" + "="*60)
    print("🧠 OMEGA v12 — PARTICLE MEMORY FIELD INTELLIGENCE SYSTEM")
    print("="*60)

    print(f"📦 Particles      : {len(particles)}")
    print(f"📡 Events         : {len(events)}")
    print(f"🌈 Trails         : {len(trails)}")
    print(f"🔥 Heat Energy    : {int(total_heat)}")
    print(f"⚡ Avg Reward     : {sum(p.reward for p in particles)/len(particles):.2f}")

    print("-"*60)
    print("🧩 LEGEND")
    print("🟣🔵🟢⚪ = particle states")
    print("✦ = event gravity node")
    print("🟥🟧🟨🟩 = memory heat field")
    print("colored dots = trail echoes")
    print("-"*60)

    print("SYSTEM CORE:")
    print("observe → attract → move → learn → reinforce → replicate → decay")
    print("="*60)

# ================================
# MAIN LOOP
# ================================
try:
    while True:
        for p in particles:
            p.step()

        decay_events()
        decay_trails()
        decay_heat()

        render()
        time.sleep(TICK_RATE)

except KeyboardInterrupt:
    clear()
    print("🧠 OMEGA v12 SAFELY SHUT DOWN")
