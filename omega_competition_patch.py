import random

def redistribute_pressure(attractors):
    keys = list(attractors.keys())

    if len(keys) < 2:
        return

    a, b = random.sample(keys, 2)

    transfer = min(attractors[a] * 0.05, 0.02)

    attractors[a] -= transfer
    attractors[b] += transfer
