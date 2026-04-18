# 🧠 Omega v14 Swarm Specialization Runtime

import time
from omega_core.omega_specialization_v14 import SpecializationEngine


engine = SpecializationEngine()

while True:

    state, scores, best, agents = engine.step()

    print("\n🧠 OMEGA v14 EMERGENT SPECIALIZATION SYSTEM")

    print("\n🌐 ENVIRONMENT")
    print(state)

    print("\n🏆 BEST PERFORMER")
    print(best)

    print("\n🧠 AGENT POPULATION")

    for k, v in agents.items():

        bar = "█" * int(v["skill"] * 20)

        print(f"{k:<25} {bar:<20} {round(v['skill'],3)} ({v['role']})")

    print("\n📊 SCORES")

    for k, v in scores.items():
        print(f"{k:<25} {round(v,3)}")

    print("\n" + "-" * 60)

    time.sleep(1)
