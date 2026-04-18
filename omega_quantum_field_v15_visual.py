import os
import time
import random
import math
import uuid

SIZE = 40
PARTICLES = 60

FIELD = {
    "pressure": 0.0,
    "coherence": 0.0,
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

def heat_char(v):
    if v > 30: return "🟥"
    if v > 20: return "🟧"
    if v > 10: return "🟨"
    if v > 5:  return "🟩"
    return None

trails = []

def add_trail(x, y):
    trails.append({
        "x": x,
        "y": y,
        "life": 6,
        "color": "✦" if random.random() < 0.5 else "●",
        "intensity": random.uniform(0.5, 1.0)
    })

def decay_trails():
    for t in trails:
        t["life"] -= 1
    trails[:] = [t for t in trails if t["life"] > 0]

class Particle:
    def __init__(self):
        self.x = random.randint(0, SIZE-1)
        self.y = random.randint(0, SIZE-1)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def step(self):
        self.vx += FIELD["entropy"] * 0.01
        self.vy += FIELD["pressure"] * 0.01

        self.x += self.vx
        self.y += self.vy

        self.x %= SIZE
        self.y %= SIZE

        update_heat(int(self.x), int(self.y))

        if random.random() < 0.08:
            add_trail(int(self.x), int(self.y))

        if abs(self.vx) > 0.3 or abs(self.vy) > 0.3:
            add_trail(int(self.x), int(self.y))

particles = [Particle() for _ in range(PARTICLES)]

def field_visual_bias():
    if FIELD["entropy"] > 0.7:
        return "✦"
    if FIELD["pressure"] > 1.5:
        return "●"
    return None

def update_field():
    FIELD["pressure"] = sum(p.vx**2 + p.vy**2 for p in particles) * 0.01
    FIELD["entropy"] = random.random()

def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for y in range(SIZE):
        for x in range(SIZE):
            v = heatmap[y][x]
            if v > 30: grid[y][x] = "🟥"
            elif v > 20: grid[y][x] = "🟧"
            elif v > 10: grid[y][x] = "🟨"
            elif v > 5: grid[y][x] = "🟩"

    for t in trails:
        grid[t["y"]][t["x"]] = t["color"]

    for p in particles:
        grid[int(p.y)][int(p.x)] = particle_color(p)

    sym = field_visual_bias()
    if sym:
        rx = random.randint(0, SIZE-1)
        ry = random.randint(0, SIZE-1)
        grid[ry][rx] = sym

    print("\033[H\033[J", end="")
    for row in grid:
        print("".join(row))

    print("\nOMEGA v15.1")

try:
    while True:
        update_field()
        for p in particles:
            p.step()
        decay_trails()
        decay_heat()
        render()
        time.sleep(0.12)
except KeyboardInterrupt:
    print("STOPPED")
