import requests
import json
import os
from dkf_v15_model_router import resolve_model

OLLAMA = "http://127.0.0.1:11434"
MEMORY = os.path.expanduser("~/Omega/dkf_swarm_memory.json")


# -----------------------------
# MEMORY SYSTEM
# -----------------------------
def load_memory():
    if not os.path.exists(MEMORY):
        return []
    try:
        return json.load(open(MEMORY))
    except:
        return []


def save_memory(mem):
    json.dump(mem[-100:], open(MEMORY, "w"))


# -----------------------------
# SWARM AGENTS
# -----------------------------
AGENTS = [
    "analyst",
    "logic_engine",
    "creative_reasoner"
]


def build_prompt(agent, user, memory):
    context = f"""
You are a swarm agent in DKF v15.

Agent role: {agent}
You must respond from your perspective.

System goal:
- analyze input
- contribute reasoning
- avoid repetition
"""

    for m in memory[-3:]:
        context += f"\nUser: {m['user']}\nAgent: {m['response']}"

    context += f"\n\nUser: {user}\n{agent}:"
    return context


# -----------------------------
# SINGLE AGENT CALL
# -----------------------------
def call_agent(agent, user, memory):
    model = resolve_model()

    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": model,
                "prompt": build_prompt(agent, user, memory),
                "stream": False
            }
        )

        return r.json().get("response", "")
    except:
        return "[agent error]"


# -----------------------------
# CONSENSUS ENGINE
# -----------------------------
def consensus(responses):
    return max(responses, key=len)


# -----------------------------
# MAIN SWARM LOOP
# -----------------------------
print("🧠 DKF v15 SWARM COGNITION BUS ONLINE")

while True:
    q = input("SWARM > ").strip()

    if q in ["exit", "quit"]:
        break

    memory = load_memory()

    results = []

    for agent in AGENTS:
        out = call_agent(agent, q, memory)
        results.append(out)

    final = consensus(results)

    memory.append({"user": q, "response": final})
    save_memory(memory)

    print("\n🧠 RESPONSE:\n")
    print(final)
    print("\n" + "-" * 60 + "\n")
