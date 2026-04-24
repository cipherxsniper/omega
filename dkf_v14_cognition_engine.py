import requests
import json
import os
from dkf_v14_model_resolver import get_model

OLLAMA = "http://127.0.0.1:11434"
MEMORY_FILE = os.path.expanduser("~/Omega/dkf_memory.json")


# -----------------------------
# MEMORY SYSTEM
# -----------------------------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory[-50:], f)


# -----------------------------
# COGNITION CORE
# -----------------------------
SYSTEM = """
You are DKF v14 Cognition Engine.
You are logical, adaptive, and self-questioning.
You may ask clarifying questions to improve reasoning.
You maintain continuity using memory context.
"""


def build_context(memory, user_input):
    context = SYSTEM + "\n\n"

    for m in memory[-5:]:
        context += f"User: {m['user']}\nDKF: {m['bot']}\n"

    context += f"\nUser: {user_input}\nDKF:"
    return context


# -----------------------------
# MAIN REASONING LOOP
# -----------------------------
def think(user_input):
    model = get_model()
    memory = load_memory()

    prompt = build_context(memory, user_input)

    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        response = r.json().get("response", "")

        memory.append({"user": user_input, "bot": response})
        save_memory(memory)

        return response

    except Exception as e:
        return f"[DKF ERROR] {e}"


# -----------------------------
# CLI
# -----------------------------
print("🧠 DKF v14 COGNITION ENGINE ONLINE")

while True:
    q = input("DKF > ").strip()
    if q in ["exit", "quit"]:
        break

    print("\n🧠", think(q), "\n")
    print("-" * 50)
