from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import json
import os
import hashlib
from collections import defaultdict, deque

# =========================
# 🧠 MEMORY FILE
# =========================

MEM_FILE = "wink_wink_brain_v4_memory.json"

short_term = deque(maxlen=120)

graph = defaultdict(lambda: {
    "count": 0,
    "reward": 0.0,
    "quality": 0.0,
    "coherence": 0.0,
    "cluster": "unknown",
    "links": defaultdict(float)
})

# =========================
# 🧠 SIMPLE SEMANTIC CLUSTERS
# =========================

CLUSTERS = {
    "stability": ["stable", "balanced", "steady"],
    "adaptation": ["adaptive", "drift", "change"],
    "memory": ["memory", "recall", "history"],
    "structure": ["system", "graph", "network"]
}

def detect_cluster(text):
    t = text.lower()
    scores = {}

    for k, words in CLUSTERS.items():
        scores[k] = sum(1 for w in words if w in t)

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "unknown"

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
                graph[k]["quality"] = v["quality"]
                graph[k]["coherence"] = v.get("coherence", 0.0)
                graph[k]["cluster"] = v.get("cluster", "unknown")
                graph[k]["links"] = defaultdict(float, v["links"])

def save():
    data = {}
    for k, v in graph.items():
        data[k] = {
            "count": v["count"],
            "reward": v["reward"],
            "quality": v["quality"],
            "coherence": v["coherence"],
            "cluster": v["cluster"],
            "links": dict(v["links"])
        }
    with open(MEM_FILE, "w") as f:
        json.dump(data, f)

# =========================
# 🧠 COHERENCE SCORE
# =========================

def coherence_score(sentence):
    cluster = detect_cluster(sentence)

    if not short_term:
        return 1.0

    last_cluster = graph[short_term[-1]]["cluster"]

    if cluster == last_cluster:
        return 1.0
    elif cluster == "unknown":
        return 0.6
    else:
        return 0.3

# =========================
# 🧠 QUALITY
# =========================

def quality_score(sentence, signal, reward):
    length = min(len(sentence) / 120, 1.0)
    stability = 1.0 - abs(signal - 0.5)

    return (length * 0.3) + (stability * 0.4) + (reward * 0.3)

# =========================
# 🧠 UPDATE GRAPH
# =========================

def update(sentence, reward, quality, coherence):
    node = h(sentence)
    cluster = detect_cluster(sentence)

    graph[node]["count"] += 1
    graph[node]["reward"] = graph[node]["reward"] * 0.85 + reward * 0.15
    graph[node]["quality"] = graph[node]["quality"] * 0.85 + quality * 0.15
    graph[node]["coherence"] = graph[node]["coherence"] * 0.85 + coherence * 0.15
    graph[node]["cluster"] = cluster

    if short_term:
        prev = short_term[-1]
        graph[prev]["links"][node] += reward * coherence

    short_term.append(node)
    save()

# =========================
# 🧠 NOVELTY
# =========================

def novelty(sentence):
    node = h(sentence)
    if node not in graph:
        return 1.0
    return max(0.0, 1.0 - graph[node]["count"] * 0.1)

# =========================
# 🧠 GENERATOR
# =========================

def generate(metrics):
    signal = metrics["signal"]
    reward = metrics["reward"]
    state = metrics["state"]

    tone = (
        "high semantic coherence flow" if signal > 0.75 else
        "balanced adaptive reasoning" if signal > 0.45 else
        "low drift observational mode"
    )

    templates = [
        f"System operates in {tone}, maintaining structured semantic flow.",
        f"Causal memory aligns under {tone}, reinforcing stable meaning clusters.",
        f"Graph transitions reflect {state} across semantic structure layers.",
        f"Adaptive reasoning continues with coherence-aware memory propagation."
    ]

    best = None
    best_score = -1

    for t in templates:
        q = quality_score(t, signal, reward)
        n = novelty(t)
        c = coherence_score(t)

        score = (q * 0.4) + (n * 0.3) + (c * 0.3)

        if score > best_score:
            best_score = score
            best = t

    update(best, reward, quality_score(best, signal, reward), coherence_score(best))

    return best

# =========================
# 🧠 OBSERVER
# =========================

def observe():
    return {
        "signal": random.uniform(0.2, 0.95),
        "reward": random.uniform(0.4, 1.0),
        "state": "ACTIVE_LEARNING"
    }

# =========================
# 🧠 BOOT
# =========================

load()

NODE_ID = "wink_wink_brain_v4.py" 
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
    m = observe()
    publish(NODE_ID, generate(m))
    time.sleep(1)
