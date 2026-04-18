
# 🧠 OMEGA v18 — GALAXY CLUSTER MEMORY SYSTEM
# Builds long-term structure from orbital attractors

import math
import random

# =========================
# GALAXY MEMORY LAYER
# =========================
galaxies = []

class Galaxy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 1.0
        self.members = []
        self.stability = 0.5

# =========================
# DISTANCE UTILITY
# =========================
def dist(ax, ay, bx, by):
    return math.sqrt((ax - bx)**2 + (ay - by)**2)

# =========================
# CLUSTER FORMATION
# =========================
def update_galaxies(attractors):

    global galaxies

    # STEP 1 — assign attractors to clusters
    for a in attractors:
        assigned = False

        for g in galaxies:
            if dist(a.x, a.y, g.x, g.y) < 6:
                g.members.append(a)
                g.mass += a.mass
                assigned = True
                break

        if not assigned:
            galaxies.append(Galaxy(a.x, a.y))

    # STEP 2 — stabilize galaxy centers
    for g in galaxies:
        if len(g.members) > 0:
            gx = sum(m.x for m in g.members) / len(g.members)
            gy = sum(m.y for m in g.members) / len(g.members)

            g.x = gx
            g.y = gy

            # stability increases with mass
            g.stability = min(1.0, len(g.members) * 0.05)

    # STEP 3 — merge overlapping galaxies
    new_galaxies = []

    for g in galaxies:
        merged = False
        for ng in new_galaxies:
            if dist(g.x, g.y, ng.x, ng.y) < 4:
                ng.members.extend(g.members)
                ng.mass += g.mass
                merged = True
                break

        if not merged:
            new_galaxies.append(g)

    galaxies = new_galaxies

# =========================
# GALAXY FIELD INFLUENCE
# =========================
def galaxy_influence(particle):

    for g in galaxies:
        dx = g.x - particle.x
        dy = g.y - particle.y
        d = math.sqrt(dx*dx + dy*dy) + 0.1

        force = g.mass / (d * d)

        particle.vx += (dx / d) * force * 0.02
        particle.vy += (dy / d) * force * 0.02

