def safe_update_edge(edges, a, b, delta=0.05):
    if a not in edges:
        edges[a] = {}

    if b not in edges[a]:
        edges[a][b] = 1.0

    edges[a][b] = min(1.0, edges[a][b] + delta)
