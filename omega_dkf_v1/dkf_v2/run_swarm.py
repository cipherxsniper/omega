from .swarm.orchestrator import SwarmOrchestrator

swarm = SwarmOrchestrator()

while True:
    q = input("SWARM > ")
    if q in ["exit", "quit"]:
        break

    print("🧠", swarm.run(q))
