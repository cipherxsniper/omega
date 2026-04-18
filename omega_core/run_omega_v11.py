from omega_core.omega_memory_graph_v10_5 import MemoryGraph
from omega_core.node_adapter_v11 import NodeAdapter
from omega_core.file_to_node_scanner_v11 import FileNodeScanner
from omega_core.evolution_pressure_v11 import pressure, state

import time

mem = MemoryGraph()
scanner = FileNodeScanner()

print("🧠 OMEGA v11 LIVE GRAPH SYSTEM ONLINE")

while True:

    nodes = scanner.scan()

    for n in nodes:

        adapter = NodeAdapter(n, mem)

        context = adapter.perceive()

        p = pressure(context)
        s = state(p)

        adapter.act(s, p)
        adapter.learn(p * 0.1)

        print(n, "→", s, round(p,3))

    time.sleep(5)
