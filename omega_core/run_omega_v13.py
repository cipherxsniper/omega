# 🧠 Omega v13 Self-Evolving ML System Runtime

import time
from omega_core.omega_evolution_orchestrator_v13 import EvolutionOrchestrator


engine = EvolutionOrchestrator()

while True:

    state, results = engine.step()

    print("\n🧠 OMEGA v13 SELF-EVOLUTION SYSTEM")

    print("\n🌐 ENVIRONMENT STATE")
    print(state)

    print("\n🧠 NODE LEARNING STATES")

    for k, v in results.items():

        print(f"\n{k}")
        print(f"score: {round(v['score'],3)}")
        print(f"reward: {round(v['reward'],3)}")
        print(f"weights: { {i: round(j,3) for i,j in v['weights'].items()} }")

    print("\n" + "-" * 60)

    time.sleep(1)
