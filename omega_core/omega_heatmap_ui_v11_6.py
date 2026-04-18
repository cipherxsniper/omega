# 🧠 Omega v11.6 Live Cognitive Field UI

import time
from omega_core.omega_propagation_v11_6 import PropagationSystem

system = PropagationSystem()

print("\n🧠 OMEGA v11.6 LIVING FIELD ENGINE ONLINE\n")

while True:

    heatmap = system.trigger_cycle()

    print("\n🔥 COGNITIVE FIELD STATE")

    for node, value in heatmap.items():
        bars = "█" * int(value * 25)
        print(f"{node:<18} {bars:<25} {value}")

    time.sleep(1)
