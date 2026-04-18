import redis
import random
import json

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

INFLUENCE_KEY = "omega:influence"
MUTATION_KEY = "omega:mutation"


# ----------------------------
# INFLUENCE SCORING
# ----------------------------
def compute_influence(event):
    payload = event.get("payload", {})

    cpu = payload.get("cpu", 0)
    mem = payload.get("memory", 0)
    load = payload.get("load", 0)

    # stability reward (lower load = more stable)
    stability = 1 - load

    score = (cpu * 0.4) + (mem * 0.3) + (load * 0.2) + (stability * 0.1)
    return round(score, 4)


def update_influence(node, score):
    r.hset(INFLUENCE_KEY, node, score)


def get_leader():
    all_nodes = r.hgetall(INFLUENCE_KEY)

    if not all_nodes:
        return None, 0

    leader = max(all_nodes.items(), key=lambda x: float(x[1]))
    return leader[0], float(leader[1])


# ----------------------------
# MUTATION ENGINE
# ----------------------------
def mutate_node(node, score):
    """
    Higher instability → higher mutation rate
    """
    mutation_rate = min(max(score, 0.05), 0.95)

    existing = r.hget(MUTATION_KEY, node)
    if existing is None:
        existing = 0.5
    else:
        existing = float(existing)

    # drift behavior slightly
    new_value = existing + random.uniform(-mutation_rate, mutation_rate) * 0.1
    new_value = min(max(new_value, 0.01), 1.0)

    r.hset(MUTATION_KEY, node, new_value)
    return round(new_value, 4)


def get_mutation(node):
    val = r.hget(MUTATION_KEY, node)
    return float(val) if val else 0.5
