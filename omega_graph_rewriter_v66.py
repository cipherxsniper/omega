import random

class OmegaGraphRewriterV66:
    def __init__(self, graph):
        self.graph = graph

    # =========================
    # EDGE HEALTH UPDATE
    # =========================
    def update_edge_health(self):
        for node in self.graph.nodes.values():
            for edge in node.links:
                edge.health = getattr(edge, "health", 1.0)
                edge.health *= (1.0 - getattr(edge, "decay", 0.01))

    # =========================
    # REWRITE RULE ENGINE
    # =========================
    def rewrite(self):
        self.update_edge_health()

        for node in self.graph.nodes.values():

            # If node is unhealthy → reduce outgoing influence
            if node.health < 0.5:
                node.links = sorted(
                    node.links,
                    key=lambda n: getattr(n, "health", 1.0)
                )

            # If node is stable → strengthen routing priority
            elif node.health > 0.8:
                node.links = sorted(
                    node.links,
                    key=lambda n: -getattr(n, "health", 1.0)
                )

        return self.summary()

    # =========================
    # SYSTEM INSIGHT FEED
    # =========================
    def summary(self):
        return {
            "graph_nodes": len(self.graph.nodes),
            "avg_node_health": self.avg_health(),
            "mode": "adaptive_rewriting_active"
        }

    def avg_health(self):
        if not self.graph.nodes:
            return 0.0
        return sum(n.health for n in self.graph.nodes.values()) / len(self.graph.nodes)
