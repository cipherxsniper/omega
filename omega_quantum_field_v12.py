from omega_visual_patch_v12 import render
from core.omega_cognition_bridge import OmegaCognitionBridge
import random
import time

# =========================
# SAFE PATCH LAYERS (INLINE)
# =========================

def stabilize(p):
    p["vx"] *= 0.98
    p["vy"] *= 0.98

    speed = (p["vx"]**2 + p["vy"]**2) ** 0.5
    if speed > 2.5:
        scale = 2.5 / speed
        p["vx"] *= scale
        p["vy"] *= scale


def apply_swarm_influence(p):
    # optional future hook (safe no-op)
    return 0.0, 0.0


def normalize_influence(inf):
    if isinstance(inf, dict):
        return inf.get("flow_x", 0.0), inf.get("flow_y", 0.0)

    if isinstance(inf, (list, tuple)) and len(inf) >= 2:
        return inf[0], inf[1]

    if isinstance(inf, (int, float)):
        return inf * 0.5, inf * 0.5

    return 0.0, 0.0


# =========================
# CORE SYSTEM
# =========================

bridge = OmegaCognitionBridge()

particles = [
    {"x": random.random(), "y": random.random(), "vx": 0.0, "vy": 0.0}
    for _ in range(80)
]


def step():
    influence = bridge.influence_factor()
    fx, fy = normalize_influence(influence)

    for p in particles:
        # cognition field input
        p["vx"] += fx + (random.random() - 0.5) * 0.01
        p["vy"] += fy + (random.random() - 0.5) * 0.01

        # optional swarm hook
        dx, dy = apply_swarm_influence(p)
        p["vx"] += dx
        p["vy"] += dy

        # stability layer
        stabilize(p)

        # movement
        p["x"] += p["vx"]
        p["y"] += p["vy"]

        p["x"] %= 1
        p["y"] %= 1


while True:
    render(particles)
    step()
    time.sleep(0.05)
