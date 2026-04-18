def build_snapshot(nodes, edges, clusters, stats):
    return {
        "nodes": nodes,
        "edges": edges,
        "clusters": clusters,
        "stats": stats,
        "version": "v11",
        "type": "omega_cognitive_snapshot"
    }
