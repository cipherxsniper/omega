class OmegaCognitionGraphV716:

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def upsert_node(self, node_id, state):
        self.nodes[node_id] = state

    def link(self, a, b, weight=1.0):
        self.edges.setdefault(a, {})[b] = weight

    def propagate(self, source_node, signal):
        # simple influence propagation model
        if source_node not in self.edges:
            return {}

        outputs = {}

        for target, weight in self.edges[source_node].items():
            outputs[target] = {
                "signal": signal,
                "weight": weight
            }

        return outputs

    def snapshot(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
