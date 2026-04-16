def reinforce_transition(graph, a, b, success):
    # strengthen or weaken connection
    if b not in graph.edges[a]:
        graph.edges[a][b] = 0.2

    if success:
        graph.edges[a][b] = min(1.0, graph.edges[a][b] + 0.08)
    else:
        graph.edges[a][b] = max(0.05, graph.edges[a][b] - 0.05)


def probabilistic_rewire(graph, a):
    import random

    # chance to create NEW edges based on node importance
    candidates = list(graph.nodes.keys())

    for b in candidates:
        if a == b:
            continue

        if b not in graph.edges[a]:
            score_a = graph.node_score.get(a, 0.5)
            score_b = graph.node_score.get(b, 0.5)

            # correlation pressure
            if abs(score_a - score_b) < 0.15:
                if random.random() < 0.05:
                    graph.edges[a][b] = 0.3

# ===== v7.4 EXECUTION LOOP PATCH =====

def apply_v74_loop_patch(graph, trace, current, health):
    from omega_emergent_patch_v74_fix import reinforce_transition, probabilistic_rewire

    # update edge based on success
    if trace and len(trace) > 0:
        prev = trace[-1]["node"]
        reinforce_transition(graph.g, prev, current, health > 0.7)

    # probabilistic graph growth
    for node in list(graph.g.nodes):
        probabilistic_rewire(graph.g, node)


# ===== END PATCH =====
