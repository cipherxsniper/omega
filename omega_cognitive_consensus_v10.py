import time
from collections import defaultdict

# =========================
# OMEGA COGNITIVE CONSENSUS LAYER v10
# =========================

GRAPH = {
    "swarm_bus": ["memory", "assistant"],
    "memory": ["assistant"],
    "emitter": ["swarm_bus"],
    "assistant": []
}

# -------------------------
# NODE STATE MODEL
# -------------------------
nodes = {
    "swarm_bus": {
        "runtime_health": 0.4,
        "semantic_health": 0.4,
        "causal_health": 0.4,
        "trust_score": 0.5
    },
    "memory": {
        "runtime_health": 0.5,
        "semantic_health": 0.5,
        "causal_health": 0.5,
        "trust_score": 0.5
    },
    "assistant": {
        "runtime_health": 0.9,
        "semantic_health": 0.9,
        "causal_health": 0.9,
        "trust_score": 0.9
    },
    "emitter": {
        "runtime_health": 0.3,
        "semantic_health": 0.3,
        "causal_health": 0.3,
        "trust_score": 0.4
    }
}

# -------------------------
# NODE SCORE COMPUTATION
# -------------------------
def compute_node_score(node):
    return (
        node["runtime_health"] * 0.4 +
        node["semantic_health"] * 0.3 +
        node["causal_health"] * 0.3
    )

# -------------------------
# INFLUENCE PROPAGATION
# -------------------------
def propagate_influence(nodes, graph):
    for parent, children in graph.items():
        for child in children:
            nodes[child]["trust_score"] += nodes[parent]["trust_score"] * 0.05
            nodes[child]["trust_score"] = min(1.0, nodes[child]["trust_score"])

# -------------------------
# CONSENSUS ENGINE
# -------------------------
def compute_consensus(nodes, graph):
    consensus = {}

    for node_id, node in nodes.items():
        base = compute_node_score(node)
        trust = node["trust_score"]

        score = base * trust

        neighbors = graph.get(node_id, [])
        if neighbors:
            neighbor_avg = sum(
                compute_node_score(nodes[n]) for n in neighbors
            ) / len(neighbors)
            score = (score * 0.7) + (neighbor_avg * 0.3)

        consensus[node_id] = round(score, 4)

    return consensus

# -------------------------
# SYSTEM STATE CLASSIFIER
# -------------------------
def classify_system(consensus):
    avg = sum(consensus.values()) / len(consensus)

    if avg > 0.75:
        return "STABLE_CONSENSUS"
    elif avg > 0.5:
        return "DEGRADED_CONSENSUS"
    elif avg > 0.25:
        return "FRAGMENTED_TRUTH"
    return "CONSENSUS_COLLAPSE"

# -------------------------
# DISPLAY ENGINE
# -------------------------
def run():
    print("\n🧠 OMEGA COGNITIVE CONSENSUS LAYER v10\n")

    propagate_influence(nodes, GRAPH)
    consensus = compute_consensus(nodes, GRAPH)
    state = classify_system(consensus)

    print("NODE SCORES:")
    for k, v in consensus.items():
        print(f"  {k:10} → {v}")

    print("\nSYSTEM STATE:")
    print(" ", state)

    avg = sum(consensus.values()) / len(consensus)
    print("\nSYSTEM MEAN:", round(avg, 4))

    if state != "STABLE_CONSENSUS":
        print("\n⚠️  SYSTEM NOT IN FULL AGREEMENT")
    else:
        print("\n🟢 SYSTEM STABLE")

if __name__ == "__main__":
    run()
