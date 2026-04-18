import numpy as np

def compute_clusters(particles):
    clusters = []

    for p in particles:
        group = [o for o in particles if np.linalg.norm(p.pos - o.pos) < 25]

        clusters.append({
            "members": group,
            "avg_jump": np.mean([g.jump for g in group]) if group else 0,
            "size": len(group),
            "dominance": len(group)
        })

    return clusters


def classify(cluster):
    if cluster["size"] > 10:
        return "memory_zone"
    elif cluster["avg_jump"] > 3:
        return "reasoning_zone"
    else:
        return "attention_zone"
