# 🧠 Omega v12 Propagation + Self Routing

import random
from omega_core.omega_routing_policy_v12 import RoutingPolicy


class Engine:

    def __init__(self):
        self.router = RoutingPolicy()

        self.state = {
            "node_attention": 0.5,
            "node_goal": 0.4,
            "node_memory": 0.3,
            "node_stability": 0.2
        }

    # ----------------------------------------
    # update system dynamics
    # ----------------------------------------
    def step(self):

        # small stochastic drift
        for k in self.state:
            self.state[k] += random.uniform(-0.03, 0.03)
            self.state[k] = max(0, min(1, self.state[k]))

        # select active cognition path
        winner, path, probs = self.router.select_path(self.state)

        # attention collapse toward selected path
        for node in self.state:

            if node in path:
                self.state[node] += 0.05
            else:
                self.state[node] -= 0.02

            self.state[node] = max(0, min(1, self.state[node]))

        return winner, path, probs, self.state
