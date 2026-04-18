from particle_stability_patch import stabilize
from particle_swarm_patch import apply_swarm_influence
from core.omega_cognition_bridge import OmegaCognitionBridge
import random
import time

bridge = OmegaCognitionBridge()

particles = [
    {"x": random.random(), "y": random.random(), "vx": 0.0, "vy": 0.0}
    for _ in range(80)
]

def normalize_influence(inf):
    if isinstance(inf, dict):
        return inf.get("flow_x", 0.0), inf.get("flow_y", 0.0)

    if isinstance(inf, (tuple, list)) and len(inf) >= 2:
        return inf[0], inf[1]

    if isinstance(inf, (int, float)):
        return inf * 0.5, inf * 0.5

    return 0.0, 0.0


def step():
    influence = bridge.influence_factor()
    fx, fy = normalize_influence(influence)

    for p in particles:
        p["vx"] += fx + (random.random() - 0.5) * 0.01
        p["vy"] += fy + (random.random() - 0.5) * 0.01

        stabilize(p)

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["x"] %= 1
        p["y"] %= 1


while True:
    step()
    time.sleep(0.05)
