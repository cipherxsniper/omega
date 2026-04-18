# 🧠 Omega v12 Self-Routing Cognitive UI

import time
from omega_core.omega_propagation_v12 import Engine

engine = Engine()

while True:

    winner, path, probs, state = engine.step()

    print("\n🧠 OMEGA v12 SELF-ROUTING COGNITION SYSTEM")

    for k, v in state.items():
        bar = "█" * int(v * 20)
        print(f"{k:<18} {bar:<20} {round(v,3)}")

    print("\n⚡ ACTIVE REASONING PATH")
    print(" → ".join(path))

    print("\n🏆 SELECTED POLICY")
    print(winner)

    print("\n📊 ROUTING PROBABILITIES")
    labels = ["A", "B", "C"]
    for i, p in enumerate(probs):
        print(f"{labels[i]}: {round(p,3)}")

    print("\n" + "-" * 60)

    time.sleep(1)
