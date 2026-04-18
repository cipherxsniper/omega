import json
import os
import time
import random
import math

MEM_PATH = "memory/omega_memory_v19.json"
REG_PATH = "memory/node_weights_v19.json"

os.makedirs("memory", exist_ok=True)


def _load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


# --------------------------
# NODE REGISTRY + WEIGHTS
# --------------------------

def get_weights():
    return _load(REG_PATH, {})


def update_weights(node, score_delta):
    weights = get_weights()

    if node not in weights:
        weights[node] = {
            "score": 1.0,
            "stability": 1.0,
            "noise": 0.0
        }

    weights[node]["score"] += score_delta
    weights[node]["score"] = max(0.1, weights[node]["score"])

    _save(REG_PATH, weights)
    return weights


def get_dominant():
    weights = get_weights()

    if not weights:
        return None

    best_node = None
    best_score = -999

    for node, w in weights.items():
        score = w["score"] - w["noise"] + w["stability"]
        if score > best_score:
            best_score = score
            best_node = node

    return best_node


# --------------------------
# MEMORY (SWARM DIFFUSION)
# --------------------------

def load_memory():
    return _load(MEM_PATH, [])


def save_memory(mem):
    _save(MEM_PATH, mem[-500:])


def add_event(event, weight=1.0):
    mem = load_memory()

    mem.append({
        "event": event,
        "weight": weight,
        "t": time.time()
    })

    save_memory(mem)


# --------------------------
# MUTATION ENGINE
# --------------------------

def mutate_score(node):
    weights = get_weights()

    if node not in weights:
        return

    drift = random.uniform(-0.05, 0.05)
    weights[node]["score"] += drift
    weights[node]["noise"] += abs(drift) * 0.5

    _save(REG_PATH, weights)
