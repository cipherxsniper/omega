# 🧬 Omega v17 Cluster Engine

class ClusterEngine:

    def assign_cluster(self, state, node_name):

        node = state.get_node(node_name)

        best_cluster = None
        best_score = 0

        for c, cluster in state.state["clusters"].items():

            score = cluster["cohesion"] * node["trust"]

            if score > best_score:
                best_score = score
                best_cluster = c

        if best_cluster:
            node["cluster"] = best_cluster
            state.state["clusters"][best_cluster]["nodes"].append(node_name)
        else:
            new_id = f"cluster_{len(state.state['clusters'])}"
            state.state["clusters"][new_id] = {
                "nodes": [node_name],
                "cohesion": 0.5,
                "energy": 1.0
            }
            node["cluster"] = new_id
