# 🧠 Omega v11.5 Live Cross-Node System

import time
from omega_core.omega_cross_node_engine_v11_5 import CrossNodeEngine

engine = CrossNodeEngine()

print("🧠 OMEGA v11.5 CROSS-NODE SYSTEM ONLINE")

while True:

    events = engine.run_cycle()

    print(f"\n--- EVENT CYCLE ({len(events)}) ---")

    for e in events[-5:]:
        print(e)

    time.sleep(1)
