import json
import os
import math

REGISTRY = "omega_version_registry.json"
GRAPH_FILE = "omega_memory_graph.json"

# =============================
# LOAD DATA
# =============================
def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

# =============================
# STRUCTURE METRICS
# =============================
def compute_metrics(snapshot):
    nodes = snapshot.get("nodes", {})
    edges = snapshot.get("edges", {})

    node_count = len(nodes)
    edge_count = sum(len(v) for v in edges.values())

    avg_degree = edge_count / max(1, node_count)

    # entropy proxy (variation in connections)
    degrees = [len(v) for v in edges.values()]
    variance = sum((d - avg_degree) ** 2 for d in degrees) / max(1, len(degrees))

    return {
        "nodes": node_count,
        "edges": edge_count,
        "avg_degree": avg_degree,
        "connectivity_variance": variance
    }

# =============================
# EVOLUTION SCORING
# =============================
def score_evolution(prev, current):
    score = 0

    # stability gain (lower variance = more stable)
    score += (prev["connectivity_variance"] - current["connectivity_variance"]) * 2

    # connectivity improvement
    score += (current["avg_degree"] - prev["avg_degree"])

    # structural growth
    score += math.log(current["nodes"] + 1) - math.log(prev["nodes"] + 1)

    return score

# =============================
# MAIN ANALYSIS
# =============================
def analyze():
    registry = load_json(REGISTRY)
    graph = load_json(GRAPH_FILE)

    versions = registry.get("versions", [])

    if len(versions) < 2:
        print("🧠 Not enough evolution history yet.")
        return

    latest = versions[-1]
    previous = versions[-2]

    prev_metrics = compute_metrics(load_json(previous["metadata"].get("graph_snapshot", {})))
    curr_metrics = compute_metrics(graph)

    evolution_score = score_evolution(prev_metrics, curr_metrics)

    print("\n==============================")
    print("🧠 OMEGA v11 EVOLUTION ANALYSIS")
    print("==============================")

    print(f"📦 Previous Version: {previous['version']}")
    print(f"📦 Current Version : {latest['version']}")

    print("\n📊 METRICS:")
    print(f"Nodes     : {curr_metrics['nodes']}")
    print(f"Edges     : {curr_metrics['edges']}")
    print(f"Avg Degree: {curr_metrics['avg_degree']:.2f}")
    print(f"Variance  : {curr_metrics['connectivity_variance']:.2f}")

    print("\n🧠 EVOLUTION SCORE:")
    print(f"Score: {evolution_score:.4f}")

    if evolution_score > 0:
        print("🟢 SYSTEM IS EVOLVING (STRUCTURAL IMPROVEMENT)")
    else:
        print("🔴 SYSTEM IS DRIFTING / DEGRADING")

    print("==============================\n")

if __name__ == "__main__":
    analyze()
