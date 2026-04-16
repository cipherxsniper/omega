class OmegaNodeSafetyV75:
    def ensure_nodes(self, graph):
        required = ["temporal", "diagnostic", "repair"]

        for node in required:
            if node not in graph.nodes:
                graph.nodes[node] = lambda m, p: {
                    "health": 0.5,
                    "output": node,
                    "signals": {"fallback": True}
                }

            if node not in graph.memory.data:
                graph.memory.data[node] = {
                    "avg_health": 0.5,
                    "runs": 0,
                    "history": []
                }
