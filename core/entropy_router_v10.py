import random
from omega.core.global_memory import GLOBAL_MEMORY

class EntropyRouterV10:
    """
    Routes information across nodes using probabilistic field dynamics.
    """

    def route(self, event):
        nodes = list(GLOBAL_MEMORY.get("node_states", {}).keys())

        if not nodes:
            return None

        # entropy weighting (stability vs exploration)
        weights = []

        for n in nodes:
            state = GLOBAL_MEMORY["node_states"].get(n, {})
            stability = state.get("stability", 0.5)

            # unstable nodes get more exploration weight
            weight = (1.0 - stability) + random.random() * 0.2
            weights.append((n, weight))

        # normalize selection
        chosen = max(weights, key=lambda x: x[1])[0]

        return {
            "target": chosen,
            "event": event,
            "mode": "entropy_routed_jump"
        }
