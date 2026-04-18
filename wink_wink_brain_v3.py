from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import json
import os
import hashlib
from collections import defaultdict, deque

# =========================
# 🧠 MEMORY SYSTEM
# =========================

MEM_FILE = "wink_wink_brain_v3_memory.json"

short_term = deque(maxlen=100)

graph = defaultdict(lambda: {
    "count": 0,
    "reward": 0.0,
    "quality": 0.0,
    "links": defaultdict(float)
})

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
                graph[k]["quality"] = v.get("quality", 0.0)
                graph[k]["links"] = defaultdict(float, v["links"])

def save():
    data = {}
    for k, v in graph.items():
        data[k] = {
            "count": v["count"],
            "reward": v["reward"],
            "quality": v["quality"],
            "links": dict(v["links"])
        }
    with open(MEM_FILE, "w") as f:
        json.dump(data, f)

# =========================
# 🧠 QUALITY SCORING ENGINE
# =========================

def quality_score(sentence, signal, reward):
    length_factor = min(len(sentence) / 120, 1.0)

    stability_factor = 1.0 - abs(signal - 0.5)

    reward_factor = reward

    return (length_factor * 0.3 +
            stability_factor * 0.4 +
            reward_factor * 0.3)

# =========================
# 🧠 GRAPH UPDATE
# =========================

def update_graph(sentence, reward, quality):
    node = h(sentence)

    graph[node]["count"] += 1
    graph[node]["reward"] = graph[node]["reward"] * 0.85 + reward * 0.15
    graph[node]["quality"] = graph[node]["quality"] * 0.85 + quality * 0.15

    if short_term:
        prev = short_term[-1]
        graph[prev]["links"][node] += reward * quality

    short_term.append(node)

    save()

# =========================
# 🧠 NOVELTY
# =========================

def novelty(sentence):
    node = h(sentence)
    if node not in graph:
        return 1.0
    return max(0.0, 1.0 - graph[node]["count"] * 0.12)

# =========================
# 🧠 INFLUENCE BIAS
# =========================

def influence_bias(node):
    g = graph[node]
    return g["reward"] * 0.6 + g["quality"] * 0.4 + sum(g["links"].values()) * 0.05

# =========================
# 🧠 SENTENCE GENERATOR (QUALITY-AWARE)
# =========================

def generate_sentence(metrics):
    signal = metrics["signal"]
    reward = metrics["reward"]
    state = metrics["state"]

    tone = (
        "high-coherence adaptive drift" if signal > 0.75 else
        "balanced learning flow" if signal > 0.45 else
        "stable observational mode"
    )

    templates = [
        f"System operates in {tone}, signal={signal:.3f}, reward={reward:.3f}.",
        f"Causal memory stabilizes under {tone}, reinforcing structured behavior.",
        f"Behavioral graph updates with weighted continuity across state transitions.",
        f"System reflects {state} with evolving coherence patterns in memory network."
    ]

    scored = []

    for t in templates:
        q = quality_score(t, signal, reward)
        n = novelty(t)
        score = (q * 0.6) + (n * 0.4)
        scored.append((score, t, q))

    scored.sort(reverse=True, key=lambda x: x[0])

    pool = scored[:3] if scored else [(0, templates[0], 0)]

    chosen = random.choice(pool)[1]
    quality = quality_score(chosen, signal, reward)

    update_graph(chosen, reward, quality)

    return chosen

# =========================
# 🧠 OBSERVER
# =========================

def analyze():
    return {
        "signal": random.uniform(0.2, 0.95),
        "reward": random.uniform(0.4, 1.0),
        "state": "ACTIVE_LEARNING"
    }

# =========================
# 🧠 BOOT
# =========================

load()

NODE_ID = "wink_wink_brain_v3.py" 
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
