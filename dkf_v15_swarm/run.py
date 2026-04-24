from core.orchestrator import SwarmOrchestrator

print("🧠 DKF v15 SWARM COGNITION ONLINE")

swarm = SwarmOrchestrator()

while True:
    try:
        q = input("DKF > ").strip()
        if q in ["exit", "quit"]:
            break

        response = swarm.process(q)
        print("\n🧠 RESPONSE:\n")
        print(response)
        print("\n" + "-"*40 + "\n")

    except KeyboardInterrupt:
        print("\n🧠 shutdown")
        break
