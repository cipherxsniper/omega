# 🧠 Omega v12.5 Live Cognition Competition Runtime

import time
from omega_core.omega_cognition_competition_v12_5 import CognitionCompetition


engine = CognitionCompetition()

state = {
    "attention": 0.5,
    "goal": 0.4
}

while True:

    # slight environmental drift
    state["attention"] += 0.02 - 0.04 * (random := __import__("random")).random()
    state["goal"] += 0.02 - 0.04 * random.random()

    state["attention"] = max(0, min(1, state["attention"]))
    state["goal"] = max(0, min(1, state["goal"]))

    winner, proposals = engine.step(state)

    print("\n🧠 OMEGA v12.5 COGNITION COMPETITION")

    print("\n📊 STATE")
    print(state)

    print("\n⚔️ COMPETING BRAINS")
    for k, v in proposals.items():
        bar = "█" * int(v * 20)
        print(f"{k:<6} {bar:<20} {round(v,3)}")

    print("\n🏆 WINNER")
    print(winner)

    print("\n" + "-" * 50)

    time.sleep(1)
