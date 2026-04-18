def apply_decay(attractors, decay=0.96):
    for k in list(attractors.keys()):
        attractors[k] *= decay

        if attractors[k] < 0.01:
            del attractors[k]


def normalize_pressure(attractors):
    total = sum(attractors.values()) or 1
    return {k: v / total for k, v in attractors.items()}
