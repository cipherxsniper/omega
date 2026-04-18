# 🧠 Omega v11.7 Dependency Flow UI

import time
from omega_flow_engine_v11_7 import FlowEngine

flow = FlowEngine()

nodes = ["node_attention", "node_goal", "node_memory", "node_stability"]

while True:

    state = {
        "node_attention": 0.35,
        "node_goal": 0.28,
        "node_memory": 0.22,
        "node_stability": 0.18
    }

    updates = flow.propagate(state)

    print("\n🧠 CAUSAL FLOW MAP\n")

    for src, targets in flow.get_flows().items():
        for dst, w in targets.items():
            print(f"{src} → {dst}   [{round(w,3)}]")

    print("\n📡 NODE UPDATES\n")

    for k, v in updates.items():
        bar = "█" * int(v * 20)
        print(f"{k:<20} {bar:<20} {round(v,3)}")

    time.sleep(1.5)
