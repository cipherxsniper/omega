# 🧠 Omega v11.9 Meta Reasoning UI

import time
from omega_core.omega_propagation_v11_9 import Engine


engine = Engine()

while True:

    state = engine.step()
    meta = engine.trace_meta()

    print("\n🧠 OMEGA META-CAUSAL FIELD")

    for k, v in state.items():
        bar = "█" * int(v * 20)
        print(f"{k:<18} {bar:<20} {round(v,3)}")

    print("\n⚡ DOMINANT META-CAUSAL RELATION")
    print(meta)

    print("\n" + "-" * 60)

    time.sleep(1)
