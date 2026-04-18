import json, time, hashlib
from collections import defaultdict

MEM_PATH = "memory/omega_memory_v16.json"

scores = defaultdict(lambda: {
    "reward": 0,
    "noise": 0,
    "stability": 0,
    "events": 0
})

def load():
    try:
        with open(MEM_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(MEM_PATH, "w") as f:
        json.dump(data, f)

def hash_event(event):
    raw = json.dumps(event, sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()[:16]

def update(event):
    node = event["node"]
    payload = event.get("payload", {})

    cpu = payload.get("cpu", 0)
    mem = payload.get("memory", 0)
    load = payload.get("load", 0)

    scores[node]["events"] += 1

    # stability reward
    stability = 1.0 - abs(load - 0.5)
    scores[node]["stability"] += stability

    # noise penalty
    noise = abs(cpu - mem)
    scores[node]["noise"] += noise

    # reward function
    reward = stability - noise
    scores[node]["reward"] += reward

    data = load()
    data[node] = scores[node]
    save(data)

def get_dominant():
    data = load()
    if not data:
        return None

    return max(data.items(), key=lambda x: x[1]["reward"])[0]
