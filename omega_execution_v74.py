from omega_emergent_graph_v74 import OmegaEmergentGraphV74

class OmegaExecutionV74:
    def __init__(self):
        self.g = OmegaEmergentGraphV74()

    def register_node(self, name, fn):
        self.g.register(name, fn)

    def connect(self, a, b, w=0.5):
        self.g.connect(a, b, w)

    def route(self, start, payload, steps=4):
        current = start
        trace = []

        for _ in range(steps):
            fn = self.g.nodes[current]
            result = fn({}, payload)

            health = result.get("health", 0.5)

            self.g.update_node_score(current, health)

            # decay + reinforce system
            self.g.decay_edges()

            next_nodes = list(self.g.edges.get(current, {}).items())

            if not next_nodes:
                break

            # weighted + node score routing
            def score(x):
                node, w = x
                return w * self.g.node_score.get(node, 1.0)

            current = max(next_nodes, key=score)[0]

            trace.append({
                "node": current,
                "result": result
            })

        return {
            "trace": trace,
            "final_node": current,
            "node_scores": self.g.node_score,
            "edges": self.g.edges
        }
