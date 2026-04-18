def compute_stability(graph, issues):
    total = len(graph)
    broken = len(issues)

    if total == 0:
        return {"global_score": 0.0}

    score = 1.0 - (broken / total)

    return {
        "global_score": round(score, 4),
        "broken_nodes": broken,
        "total_nodes": total
    }
