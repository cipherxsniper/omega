# 🧠 Unified Graph Connector (v11.3 FIX)

from omega_core.omega_memory_graph_v10_5 import MemoryGraph

class GraphConnector:

    def __init__(self):
        self.mem = MemoryGraph()

    def get_nodes(self):
        return self.mem.state.get("nodes", {})

    def compute_pressure(self, node):

        n = self.mem.state["nodes"].get(node, {})

        base = n.get("influence", 0.5)
        stability = 1 - n.get("influence", 0.5)

        return (base * 0.6) + (stability * 0.4)
