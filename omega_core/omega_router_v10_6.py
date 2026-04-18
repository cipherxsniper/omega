from omega_core.omega_memory_graph_v10_5 import MemoryGraph
from omega_core.omega_evolution_v10_5 import pressure, state
from omega_core.omega_discovery_v10_6 import DiscoveryEngine
import time

class Router:

    def __init__(self):
        self.m = MemoryGraph()
        self.d = DiscoveryEngine()
        self.nodes = ["memory","goal","attention","stability"]

    def tick(self):

        # 1. scan filesystem (bounded)
        new_files = self.d.scan()

        for f in new_files:
            node_name = f.split("/")[-1].replace(".py","")
            if node_name not in self.nodes:
                self.nodes.append(node_name)

                self.m.write("system", f"NEW_NODE:{node_name}", 0.7)

        # 2. evaluate nodes
        out = {}

        for n in self.nodes:
            node = self.m.node(n)

            p = pressure(node)
            s = state(p)

            self.m.write(n, s, p)

            out[n] = {"pressure": p, "state": s}

        return out
