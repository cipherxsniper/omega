# 🧠 OMEGA v19 — DARK MATTER FIELD

import math
from collections import defaultdict

dark_field = defaultdict(float)
hidden_attractors = []

# ---------------------------
# UNIFIED PARTICLE ACCESS
# ---------------------------

def get(p, key):
    if isinstance(p, dict):
        return p.get(key, 0.0)
    return getattr(p, key, 0.0)

def setv(p, key, value):
    if isinstance(p, dict):
        p[key] = value
    else:
        setattr(p, key, value)

# ---------------------------
# DARK MATTER FIELD BUILD
# ---------------------------

def accumulate_dark_field(particles):
    for p in particles:
        x = int(get(p, "x") // 5)
        y = int(get(p, "y") // 5)
        dark_field[(x, y)] += 1.0

def dark_gravity(p):
    x = int(get(p, "x") // 5)
    y = int(get(p, "y") // 5)

    fx, fy = 0.0, 0.0

    for (dx, dy), intensity in dark_field.items():
        ddx = dx - x
        ddy = dy - y
        dist = math.sqrt(ddx*ddx + ddy*ddy) + 0.001

        force = intensity / (dist * dist)

        fx += ddx * force
        fy += ddy * force

    setv(p, "vx", get(p, "vx") + fx * 0.002)
    setv(p, "vy", get(p, "vy") + fy * 0.002)

# ---------------------------
# HIDDEN ATTRACTOR EMERGENCE
# ---------------------------

class HiddenAttractor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 1.0
        self.age = 0

    def evolve(self):
        self.mass += 0.01
        self.age += 1


def detect_hidden_attractors(particles):
    # cluster density emergence
    grid = defaultdict(int)

    for p in particles:
        key = (int(get(p, "x") // 10), int(get(p, "y") // 10))
        grid[key] += 1

    for (x, y), count in grid.items():
        if count > 8:
            hidden_attractors.append(HiddenAttractor(x, y))


def hidden_attractor_force(p):
    fx, fy = 0.0, 0.0

    for h in hidden_attractors:
        dx = h.x - get(p, "x")
        dy = h.y - get(p, "y")

        dist = math.sqrt(dx*dx + dy*dy) + 0.001
        force = h.mass / (dist * dist)

        fx += dx * force
        fy += dy * force

    setv(p, "vx", get(p, "vx") + fx * 0.01)
    setv(p, "vy", get(p, "vy") + fy * 0.01)

# ---------------------------
# MAIN STEP
# ---------------------------

def step_dark_matter_system(particles):
    accumulate_dark_field(particles)
    detect_hidden_attractors(particles)

    for p in particles:
        dark_gravity(p)
        hidden_attractor_force(p)

    for h in hidden_attractors:
        h.evolve()

    return particles
