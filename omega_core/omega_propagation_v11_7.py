# 🧠 Omega v11.7 Causal Propagation Controller

from omega_core.omega_dependency_graph_v11_7 import DependencyGraph

class PropagationSystem:

    def __init__(self):

        self.graph = DependencyGraph()

        self.state = {
            "node_attention": 0.5,
            "node_goal": 0.3,
            "node_memory": 0.2,
            "node_stability": 0.1
        }

    def trigger_cycle(self):

        # 🔁 propagate signals through dependency graph
        new_state = self.graph.propagate(self.state)

        # merge states (feedback loop)
        for k in self.state:
            self.state[k] = (self.state.get(k, 0) * 0.6 +
                             new_state.get(k, 0) * 0.4)

        return self.state, self.graph.get_recent_flows()
