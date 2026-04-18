from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import json
import os
import hashlib
from collections import defaultdict, deque

# =========================
# 🧠 PERSISTENT MEMORY FILE
# =========================

MEM_FILE = "wink_wink_brain_v2_memory.json"

short_term = deque(maxlen=100)

# =========================
# 🧠 CAUSAL MEMORY GRAPH
# =========================
# node = sentence hash
# edge = influence between sentences
graph = defaultdict(lambda: {"count": 0, "reward": 0.0, "links": defaultdict(float)})

# =========================
# 🧠 UTILITIES
# =========================

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

def load():
    global graph
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                graph[k]["count"] = v["count"]
                graph[k]["reward"] = v["reward"]
                graph[k]["links"] = defaultdict(float, v["links"])

def save():
    data = {}
    for k, v in graph.items():
        data[k] = {
            "count": v["count"],
            "reward": v["reward"],
            "links": dict(v["links"])
        }
    with open(MEM_FILE, "w") as f:
        json.dump(data, f)

# =========================
# 🧠 CAUSAL UPDATE
# =========================

def update_graph(sentence, reward):
    node = h(sentence)

    graph[node]["count"] += 1
    graph[node]["reward"] = (
        graph[node]["reward"] * 0.9 + reward * 0.1
    )

    # link to previous sentence (causal chain)
    if short_term:
        prev = short_term[-1]
        graph[prev]["links"][node] += reward

    short_term.append(node)

    save()

# =========================
# 🧠 NOVELTY SCORING
# =========================

def novelty(sentence):
    node = h(sentence)
    if node not in graph:
        return 1.0
    return max(0.0, 1.0 - graph[node]["count"] * 0.15)

# =========================
# 🧠 CAUSAL INFLUENCE SCORE
# =========================

def influence_score(node):
    return graph[node]["reward"] + sum(graph[node]["links"].values()) * 0.1

# =========================
# 🧠 SENTENCE ENGINE (v2)
# =========================

def generate_sentence(metrics):
    signal = metrics["signal"]
    reward = metrics["reward"]
    state = metrics["state"]

    tone = (
        "high adaptive drift" if signal > 0.75 else
        "moderate learning flow" if signal > 0.45 else
        "stable observational mode"
    )

    templates = [
        f"System enters {tone}, signal={signal:.3f}, reward={reward:.3f}.",
        f"Causal graph updates under {tone} with memory reinforcement.",
        f"Behavioral node influence propagates through causal memory network.",
        f"State transition observed: {state} with evolving structural dependency."
    ]

    scored = []

    for t in templates:
        score = novelty(t)
        scored.append((score, t))

    scored.sort(reverse=True, key=lambda x: x[0])

    pool = [t for s, t in scored if s > 0]

    if not pool:
        pool = templates

    chosen = random.choice(pool)

    update_graph(chosen, reward)

    return chosen

# =========================
# 🧠 OBSERVER CORE LOOP
# =========================

def analyze():
    # replace later with real engine metrics
    return {
        "signal": random.uniform(0.2, 0.95),
        "reward": random.uniform(0.4, 1.0),
        "state": "ACTIVE_LEARNING"
    }

# =========================
# 🧠 BOOT
# =========================

load()

NODE_ID = "wink_wink_brain_v2.py" 
register(NODE_ID)

while True:
    def anti_loop(msg, hist):
        return msg not in hist[-10:]

    history = []
    recent = fetch_recent(5)
    if recent:
        influence = sum(m["signal"] for m in recent) / len(recent)
        try:
            signal = (signal + influence) / 2
        except:
            pass
    metrics = analyze()
    publish(NODE_ID, generate_sentence(metrics))
    time.sleep(1)
