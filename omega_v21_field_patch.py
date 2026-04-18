import math

def normalize_field(attractor_map):
    total = sum(attractor_map.values()) or 1
    return {k: v / total for k, v in attractor_map.items()}


def decay_field(attractor_map, decay=0.97):
    for k in list(attractor_map.keys()):
        attractor_map[k] *= decay
        if attractor_map[k] < 0.01:
            del attractor_map[k]
