
# 🧠 OMEGA v17 — ORBITAL ATTRACTOR FIELD
# Adds gravitational orbit physics without breaking v16 render contract

import math
import random

# =========================
# ORBITAL ATTRACTOR SYSTEM
# =========================
orbit_nodes = []

class Attractor:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.spin = random.uniform(-1, 1)
        self.radius = random.uniform(2, 6)

# =========================
# ORBIT PHYSICS ENGINE
# =========================
def apply_orbits(particles):
    for p in particles:
        for a in orbit_nodes:

            dx = a.x - p.x
            dy = a.y - p.y
            dist = math.sqrt(dx*dx + dy*dy) + 0.1

            # gravity attraction
            force = a.mass / (dist * dist)

            # tangential orbit force (key emergence mechanic)
            tx = -dy / dist
            ty = dx / dist

            p.vx += (dx / dist) * force * 0.05
            p.vy += (dy / dist) * force * 0.05

            p.vx += tx * a.spin * 0.02
            p.vy += ty * a.spin * 0.02

# =========================
# ORBIT SEEDING (FROM EVENTS)
# =========================
def maybe_create_attractor(x, y, strength):
    if strength > 1.2 and random.random() < 0.08:
        orbit_nodes.append(Attractor(x, y, strength))

# =========================
# ATTRACTOR DECAY SYSTEM
# =========================
def decay_attractors():
    for a in orbit_nodes:
        a.mass *= 0.995

    orbit_nodes[:] = [a for a in orbit_nodes if a.mass > 0.2]

# =========================
# INTEGRATION HOOK (CALL THIS IN MAIN LOOP)
# =========================
def step_orbit_system(particles):
    apply_orbits(particles)
    decay_attractors()

