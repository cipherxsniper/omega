import requests
from dkf_v15_swarm_bus import call_agent, AGENTS, load_memory

OLLAMA = "http://127.0.0.1:11434"


def run_swarm(query):
    memory = load_memory()
    outputs = []

    for a in AGENTS:
        outputs.append(call_agent(a, query, memory))

    # simple fusion
    return max(outputs, key=len)


print("🧠 DKF v16 RUNTIME BRIDGE ONLINE")

while True:
    q = input("DKF > ").strip()

    if q in ["exit", "quit"]:
        break

    print("\n🧠", run_swarm(q), "\n")
    print("-" * 50)
