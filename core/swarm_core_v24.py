import redis
import json
import math
from collections import defaultdict

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MEMORY_KEY = "omega:memory"
WEIGHT_KEY = "omega:weights"
CLUSTER_KEY = "omega:clusters"


# -----------------------------
# VECTOR DISTANCE (CLUSTERING)
# -----------------------------
def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# -----------------------------
# EMERGENT CLUSTER DETECTION
# -----------------------------
def build_clusters(memory, threshold=0.15):
    clusters = []

    for item in memory:
        placed = False
        vec = item["vector"]

        for cluster in clusters:
            if distance(vec, cluster["center"]) < threshold:
                cluster["items"].append(item)
                cluster["center"] = [
                    (c + v) / 2 for c, v in zip(cluster["center"], vec)
                ]
                placed = True
                break

        if not placed:
            clusters.append({
                "center": vec,
                "items": [item]
            })

    return clusters


# -----------------------------
# MEMORY DIFFUSION
# -----------------------------
def diffuse_memory(memory, clusters):
    influence_map = defaultdict(float)

    for i, cluster in enumerate(clusters):
        weight = len(cluster["items"]) / max(len(memory), 1)

        for item in cluster["items"]:
            node = item["event"].get("node", "unknown")
            influence_map[node] += weight

    return dict(influence_map)


# -----------------------------
# SWARM LEARNING WEIGHTS
# -----------------------------
def update_weights(influence_map):
    for node, score in influence_map.items():
        existing = r.hget(WEIGHT_KEY, node)

        if existing is None:
            existing = 0.5
        else:
            existing = float(existing)

        # adaptive learning rule
        new_weight = existing + (score - existing) * 0.2

        r.hset(WEIGHT_KEY, node, round(new_weight, 4))


# -----------------------------
# STORE CLUSTERS
# -----------------------------
def store_clusters(clusters):
    compact = [
        {
            "size": len(c["items"]),
            "center": c["center"]
        }
        for c in clusters
    ]

    r.set(CLUSTER_KEY, json.dumps(compact))
