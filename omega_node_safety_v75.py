class OmegaNodeSafetyV75:
    def ensure_nodes(self, graph):
        required = ["temporal", "diagnostic", "repair"]

        for node in required:
            # ensure node exists
            if node not in graph.nodes:
                graph.nodes[node] = lambda m, p: {
                    "health": 0.5,
                    "output": node,
                    "signals": {"fallback": True}
                }

            # ensure memory exists using SAFE access
            try:
                mem = graph.memory.get(node)
            except Exception:
                mem = None

            if not mem:
                # create memory using record system
                graph.memory.record(node, {}, {"health": 0.5})
