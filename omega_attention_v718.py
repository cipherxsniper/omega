class OmegaAttentionV718:

    def __init__(self):
        self.node_weights = {}

    def score_event(self, event, graph_state):
        base = {
            "success": 1.0,
            "state_update": 0.7,
            "route_error": 1.8,
            "contract_violation": 2.5
        }.get(event.get("event_type"), 1.0)

        node = event.get("node")
        node_bias = self.node_weights.get(node, 1.0) if node else 1.2

        return base * node_bias

    def update_attention(self, event):
        node = event.get("node")
        if not node:
            return

        # reinforce attention on active nodes
        self.node_weights[node] = self.node_weights.get(node, 1.0) * 1.05

        # cap explosion
        if self.node_weights[node] > 3.0:
            self.node_weights[node] = 3.0

    def decay_attention(self):
        for k in list(self.node_weights.keys()):
            self.node_weights[k] *= 0.98

            if self.node_weights[k] < 0.3:
                del self.node_weights[k]
