import os
import time
import random
from collections import defaultdict, deque
from hashlib import md5

print("🧠 WINK_WINK v11 CAUSAL REASONING ENGINE ONLINE")

# -----------------------------
# MEMORY + CAUSAL STATE
# -----------------------------
memory = {
    "events": deque(maxlen=200),
    "seen_hashes": set(),
    "causal_graph": defaultdict(lambda: defaultdict(float)),
    "last_state": {}
}

NODE_COUNT = 250

nodes = [
    {"id": i, "state": random.random(), "bias": random.uniform(0.2, 0.8)}
    for i in range(NODE_COUNT)
]

# -----------------------------
# FILE SEMANTIC EXTRACTION
# -----------------------------
def scan_files(limit=120):
    files_data = []

    for root, _, files in os.walk("."):
        for f in files[:limit]:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", errors="ignore") as file:
                        text = file.read(3000)

                    features = {
                        "memory": text.count("memory"),
                        "node": text.count("node"),
                        "swarm": text.count("swarm"),
                        "kernel": text.count("kernel"),
                        "learning": text.count("learn"),
                        "event": text.count("event")
                    }

                    score = sum(features.values())

                    files_data.append({
                        "file": f,
                        "features": features,
                        "score": score
                    })

                except:
                    continue

    return files_data

# -----------------------------
# NODE DYNAMICS (CAUSAL PROPAGATION)
# -----------------------------
def update_nodes():
    total = 0

    for n in nodes:
        influence = random.uniform(-0.04, 0.04)

        # causal drift
        n["state"] += influence * n["bias"]
        n["state"] = max(0, min(1, n["state"]))

        total += n["state"]

    return total / NODE_COUNT

# -----------------------------
# CAUSAL GRAPH BUILDER
# -----------------------------
def build_causal_graph(files):
    graph = defaultdict(float)

    for f in files:
        feat = f["features"]

        if feat["memory"] > 0:
            graph["memory -> reasoning"] += 1
        if feat["node"] > 0:
            graph["node -> swarm"] += 1
        if feat["kernel"] > 0:
            graph["kernel -> execution"] += 1
        if feat["learning"] > 0:
            graph["learning -> adaptation"] += 1
        if feat["event"] > 0:
            graph["event -> memory"] += 1

    return graph

# -----------------------------
# CAUSAL STATE ANALYSIS
# -----------------------------
def analyze_state(graph, signal):
    strongest = max(graph.items(), key=lambda x: x[1])[0] if graph else "unknown"

    if signal > 0.75:
        state = "COHERENT CAUSAL FLOW"
        reason = "feedback loops stabilizing across node network"
    elif signal > 0.55:
        state = "STRUCTURED VARIATION"
        reason = "controlled divergence in subsystem interaction"
    elif signal > 0.35:
        state = "EXPLORATORY DYNAMICS"
        reason = "causal uncertainty increasing between modules"
    else:
        state = "HIGH ENTROPY STATE"
        reason = "unstable propagation across system graph"

    return state, reason, strongest

# -----------------------------
# NOVELTY CONTROL (NO REPETITION)
# -----------------------------
def novelty_hash(text):
    return md5(text.encode()).hexdigest()

def unique(text):
    h = novelty_hash(text)
    if h in memory["seen_hashes"]:
        return False
    memory["seen_hashes"].add(h)
    return True

# -----------------------------
# STRUCTURED ENGLISH GENERATOR
# -----------------------------
def generate_thought(state, reason, strongest, files, signal):

    base = [
        f"The system is observing causal structure in {strongest}.",
        f"Execution behavior suggests interaction between {strongest} and system memory.",
        f"Node dynamics indicate that {strongest} is influencing global coherence.",
        f"Omega is mapping causal dependencies centered on {strongest}."
    ]

    reasoning_layer = [
        f"This is driven by {reason}.",
        f"The signal level ({round(signal,3)}) modifies interpretation stability.",
        f"File activity suggests structural reinforcement patterns.",
        f"System feedback loops are emerging across distributed components."
    ]

    for _ in range(10):
        sentence = random.choice(base) + " " + random.choice(reasoning_layer)

        if unique(sentence):
            return sentence

    return "System is stabilizing without new causal variation detected."

# -----------------------------
# EVENT TRACKER
# -----------------------------
def record_event(tick, state, signal, strongest):
    memory["events"].append({
        "tick": tick,
        "state": state,
        "signal": signal,
        "strongest": strongest
    })

# -----------------------------
# MAIN LOOP
# -----------------------------
tick = 0

while True:

    files = scan_files()
    graph = build_causal_graph(files)
    signal = update_nodes()

    state, reason, strongest = analyze_state(graph, signal)
    thought = generate_thought(state, reason, strongest, len(files), signal)

    record_event(tick, state, signal, strongest)

    print(f"\n🧠 TICK {tick}")
    print(f"FILES={len(files)} | SIGNAL={round(signal,3)}")
    print(f"STATE={state}")
    print(f"CAUSE={reason}")
    print(f"DOMINANT={strongest}")
    print(f"THOUGHT={thought}")

    tick += 1
    time.sleep(1)
