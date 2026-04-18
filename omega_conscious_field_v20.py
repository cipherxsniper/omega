# 🧠 OMEGA v20 — EVENT CONSCIOUSNESS LAYER

import math
from collections import defaultdict

# ---------------------------
# OBSERVATION FIELD
# ---------------------------

observation_field = defaultdict(float)
attention_nodes = []

def register_observation(x, y, intensity=1.0):
    key = (int(x // 5), int(y // 5))
    observation_field[key] += intensity

def decay_observation():
    for k in list(observation_field.keys()):
        observation_field[k] *= 0.98
        if observation_field[k] < 0.01:
            del observation_field[k]

# ---------------------------
# "AWARE" PARTICLE RESPONSE MODEL
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
# CONSCIOUS BEHAVIOR SHIFT
# ---------------------------

def consciousness_response(p):
    x = get(p, "x")
    y = get(p, "y")

    cell = (int(x // 5), int(y // 5))
    awareness = observation_field.get(cell, 0.0)

    vx = get(p, "vx")
    vy = get(p, "vy")

    # ---------------------------
    # BEHAVIOR MODULATION
    # ---------------------------

    if awareness > 5.0:
        # HIGH OBSERVATION: particle becomes "controlled"
        vx *= 0.92
        vy *= 0.92

        # stabilize trajectory (less chaos)
        vx += math.sin(x * 0.01) * 0.1
        vy += math.cos(y * 0.01) * 0.1

    elif awareness > 1.0:
        # MEDIUM OBSERVATION: cautious drift
        vx *= 0.98
        vy *= 0.98

    else:
        # LOW OBSERVATION: free chaotic motion
        vx += (math.sin(y) - math.cos(x)) * 0.02

    setv(p, "vx", vx)
    setv(p, "vy", vy)

# ---------------------------
# ATTENTION EMERGENCE SYSTEM
# ---------------------------

def generate_attention_nodes(particles):
    # clusters of repeated observation become "nodes"
    heat = defaultdict(int)

    for p in particles:
        key = (int(get(p, "x") // 10), int(get(p, "y") // 10))
        heat[key] += 1

    for (x, y), h in heat.items():
        if h > 10:
            attention_nodes.append((x, y))

# ---------------------------
# MAIN STEP
# ---------------------------

def step_conscious_field(particles):
    decay_observation()
    generate_attention_nodes(particles)

    for p in particles:
        consciousness_response(p)

    return particles
