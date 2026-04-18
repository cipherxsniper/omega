from omega_core.omega_memory_graph_v10_5 import MemoryGraph
from omega_core.omega_evolution_v10_5 import pressure, state

class Router:
    def __init__(self):
        self.m=MemoryGraph()

    def tick(self,nodes):
        out={}
        for n in nodes:
            node=self.m.node(n)
            p=pressure(node)
            s=state(p)

            self.m.write(n,s,p)

            out[n]={"pressure":p,"state":s}
        return out
