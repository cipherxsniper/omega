from particle_stability_patch import stabilize
from particle_swarm_patch import apply_swarm_influence
from core.omega_cognition_bridge import OmegaCognitionBridge

import random
import time
import math
import os

bridge = OmegaCognitionBridge()

SIZE = 40
PARTICLES = 80

particles = [
    {"x": random.randint(0, SIZE-1), "y": random.randint(0, SIZE-1), "vx": 0.0, "vy": 0.0}
    for _ in range(PARTICLES)
]

def normalize_influence(inf):
    if isinstance(inf, dict):
        return inf.get("flow_x", 0.0), inf.get("flow_y", 0.0)
    return float(inf), float(inf)

def render():
    grid = [[" " for _ in range(SIZE)] for _ in range(SIZE)]

    for p in particles:
        x = int(p["x"]) % SIZE
        y = int(p["y"]) % SIZE
        grid[y][x] = "●"

    os.system("clear")

    for row in grid:
        print("".join(row))

    print("\n🧠 OMEGA FIELD ACTIVE")
    print(f"Particles: {len(particles)}")

def step():
    influence = bridge.influence_factor()
    fx, fy = normalize_influence(influence)

    for p in particles:

        p["vx"] += fx + (random.random() - 0.5) * 0.02
        p["vy"] += fy + (random.random() - 0.5) * 0.02

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["vx"] *= 0.98
        p["vy"] *= 0.98

        p["x"] %= SIZE
        p["y"] %= SIZE

def loop():
    while True:
        step()
        render()
        time.sleep(0.08)

if __name__ == "__main__":
    print("🧠⚛️ OMEGA FIELD VISUAL ENGINE ONLINE")
    time.sleep(0.5)
    loop()
