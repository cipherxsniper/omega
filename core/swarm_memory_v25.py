import json
import time
import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MEMORY_KEY = "omega:swarm:events"
WEIGHTS_KEY = "omega:swarm:weights"
LEADER_KEY  = "omega:swarm:leader"


# ----------------------------
# EVENT STREAM (Redis list)
# ----------------------------
def store_event(node, vector, event):
    payload = {
        "node": node,
        "vector": vector,
        "event": event,
        "ts": time.time()
    }
    r.rpush(MEMORY_KEY, json.dumps(payload))


def load_events(limit=500):
    raw = r.lrange(MEMORY_KEY, -limit, -1)
    return [json.loads(x) for x in raw]


# ----------------------------
# CLUSTER WEIGHT UPDATE
# ----------------------------
def update_weight(src, dst, score):
    key = f"{WEIGHTS_KEY}:{src}:{dst}"
    cur = float(r.get(key) or 0.0)
    r.set(key, cur * 0.9 + score * 0.1)


def get_weights():
    keys = r.keys(f"{WEIGHTS_KEY}:*")
    return {k: float(r.get(k)) for k in keys}


# ----------------------------
# CLUSTER DETECTION (simple centroid grouping)
# ----------------------------
def cluster_events(events):
    clusters = []

    for e in events:
        v = e.get("vector", [])
        placed = False

        for c in clusters:
            if abs(sum(c["centroid"]) / len(c["centroid"]) - sum(v) / max(len(v),1)) < 0.5:
                c["events"].append(e)
                c["centroid"].extend(v)
                placed = True
                break

        if not placed:
            clusters.append({
                "centroid": v.copy(),
                "events": [e]
            })

    return clusters


# ----------------------------
# LEADER ELECTION (highest avg reward node)
# ----------------------------
def elect_leader(events):
    scores = {}

    for e in events:
        node = e.get("node")
        reward = e.get("event", {}).get("reward", 0)

        scores[node] = scores.get(node, 0) + reward

    if not scores:
        return None

    return max(scores, key=scores.get)
