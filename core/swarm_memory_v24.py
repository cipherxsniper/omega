import json
import redis
import time

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MEMORY_KEY = "omega:swarm:memory"
WEIGHTS_KEY = "omega:swarm:weights"


def store_event(node, vector, event):
    payload = {
        "node": node,
        "vector": json.dumps(vector),
        "event": json.dumps(event),
        "ts": time.time()
    }
    r.rpush(MEMORY_KEY, json.dumps(payload))


def load_memory(limit=500):
    raw = r.lrange(MEMORY_KEY, -limit, -1)
    return [json.loads(x) for x in raw]


def update_weight(src, dst, score):
    key = f"{WEIGHTS_KEY}:{src}:{dst}"
    current = float(r.get(key) or 0)
    r.set(key, current * 0.9 + score * 0.1)


# -------------------------
# ADD THESE (MISSING FIX)
# -------------------------

def diffuse_event(event, score):
    if score > 0.4:
        r.publish("omega.diffusion", json.dumps({
            "event": event,
            "score": score
        }))


def elect_leader():
    keys = r.keys(f"{WEIGHTS_KEY}:*")

    scores = {}

    for k in keys:
        val = float(r.get(k) or 0)
        node = k.split(":")[-1]
        scores[node] = scores.get(node, 0) + val

    if not scores:
        return None

    leader = max(scores, key=scores.get)
    r.set("omega:swarm:leader", leader)

    return leader


# =========================
# MISSING SWARM FUNCTIONS FIX
# =========================

def diffuse_event(event, score):
    # simple diffusion placeholder (no-op safe version)
    return {
        "event": event,
        "score": score,
        "diffused": True
    }


def elect_leader():
    # simple leader election placeholder
    return "python-node-1"
