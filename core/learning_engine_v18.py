import json
import time
import math
import os

MEM_PATH = "memory/omega_memory_v18.json"

os.makedirs("memory", exist_ok=True)


def _load():
    if not os.path.exists(MEM_PATH):
        return []
    with open(MEM_PATH, "r") as f:
        return json.load(f)


def _save(data):
    with open(MEM_PATH, "w") as f:
        json.dump(data[-500:], f)  # keep last 500 events


def _vector(event):
    p = event.get("payload", {})
    cpu = p.get("cpu", 0)
    mem = p.get("memory", 0)
    load = p.get("load", 0)

    node_hash = abs(hash(event.get("node", ""))) % 1000 / 1000
    t = event.get("timestamp", time.time()) % 1000 / 1000

    return [cpu, mem, load, node_hash, t]


def _similarity(v1, v2):
    dot = sum(a*b for a,b in zip(v1,v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(a*a for a in v2))
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 * mag2)


def update(event):
    memory = _load()

    vec = _vector(event)

    # duplicate detection
    for old in memory[-50:]:
        old_vec = old["vector"]
        sim = _similarity(vec, old_vec)
        if sim > 0.97:
            return "DUPLICATE_SUPPRESSED"

    memory.append({
        "event": event,
        "vector": vec,
        "timestamp": time.time()
    })

    _save(memory)
    return "LEARNED"


def recall(event):
    memory = _load()
    vec = _vector(event)

    best = None
    best_score = 0

    for m in memory[-100:]:
        sim = _similarity(vec, m["vector"])
        if sim > best_score:
            best_score = sim
            best = m

    return best, best_score
