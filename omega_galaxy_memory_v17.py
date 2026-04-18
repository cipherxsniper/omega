# 🧠 OMEGA v17 — GALAXY CLUSTER MEMORY SYSTEM

import math
from collections import defaultdict

class GalaxyCluster:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.mass = 1.0
        self.particles = []
        self.history_strength = 0.0

    def absorb(self, p):
        self.particles.append(p)
        self.mass += 0.1
        self.history_strength += 1.0

    def center_of_mass(self):
        if not self.particles:
            return self.x, self.y
        x = sum(p["x"] for p in self.particles) / len(self.particles)
        y = sum(p["y"] for p in self.particles) / len(self.particles)
        return x, y


galaxies = []

def detect_galaxy_clusters(particles, threshold=5):
    clusters = defaultdict(list)

    for p in particles:
        key = (int(p["x"] / threshold), int(p["y"] / threshold))
        clusters[key].append(p)

    for k, group in clusters.items():
        if len(group) >= 3:
            gx = sum(p["x"] for p in group) / len(group)
            gy = sum(p["y"] for p in group) / len(group)

            g = GalaxyCluster(len(galaxies), gx, gy)
            for p in group:
                g.absorb(p)

            galaxies.append(g)

    return galaxies


def galaxy_influence(particle):
    # gravity from galaxy memory cores
    fx, fy = 0.0, 0.0

    for g in galaxies:
        dx = g.x - particle["x"]
        dy = g.y - particle["y"]
        dist = math.sqrt(dx*dx + dy*dy) + 0.001

        force = g.mass / (dist * dist)

        fx += dx * force
        fy += dy * force

    particle["vx"] += fx * 0.01
    particle["vy"] += fy * 0.01

    return particle


def step_galaxy_system(particles):
    detect_galaxy_clusters(particles)

    for p in particles:
        galaxy_influence(p)

    return particles
