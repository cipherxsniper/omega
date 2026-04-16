import time
import math

class SwarmIntelligenceRouterV772:
    def __init__(self):
        # node_id -> metrics
        self.peers = {}

    def update_peer(self, node_id, latency=0.1, trust=0.5, hops=1):
        """
        latency: lower is better
        trust: higher is better (0-1)
        hops: lower is better
        """

        self.peers[node_id] = {
            "latency": latency,
            "trust": trust,
            "hops": hops,
            "last_seen": time.time()
        }

    def score_peer(self, metrics):
        """
        Higher score = better routing target
        """

        latency_score = 1 / (metrics["latency"] + 0.01)
        trust_score = metrics["trust"] * 10
        hop_penalty = 1 / (metrics["hops"] + 1)

        return latency_score + trust_score + hop_penalty

    def select_best_peer(self):
        if not self.peers:
            return None

        best_node = None
        best_score = -1

        for node_id, metrics in self.peers.items():
            score = self.score_peer(metrics)

            if score > best_score:
                best_score = score
                best_node = node_id

        return best_node, best_score

    def route(self, message):
        best = self.select_best_peer()

        if not best:
            return {
                "status": "no_peers",
                "action": "broadcast_fallback"
            }

        node_id, score = best

        return {
            "status": "routed",
            "target": node_id,
            "score": score,
            "message": message
        }
