import os
import time
import json
import requests

OLLAMA = "http://127.0.0.1:11434"

STATE = os.path.expanduser("~/Omega/dkf_v17_state.json")
MEMORY = os.path.expanduser("~/Omega/dkf_v17_memory.json")


def init():
    for f, d in [(STATE, {}), (MEMORY, [])]:
        if not os.path.exists(f):
            with open(f, "w") as x:
                json.dump(d, x)


def load(path, default):
    try:
        return json.load(open(path))
    except:
        return default


# ✅ FIXED SAVE FUNCTION
def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def ollama_alive():
    try:
        return requests.get(f"{OLLAMA}/api/tags", timeout=2).status_code == 200
    except:
        return False


def restart():
    print("🔁 Ollama recovery triggered")
    os.system("pkill ollama")
    time.sleep(1)
    os.system("ollama serve &")


def model():
    try:
        r = requests.get(f"{OLLAMA}/api/tags", timeout=3)
        ms = r.json().get("models", [])
        return ms[0]["name"] if ms else "tinyllama:latest"
    except:
        return "tinyllama:latest"


def ask(prompt):
    try:
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": model(),
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return r.json().get("response", "")
    except Exception as e:
        return f"[error] {e}"


def run():
    init()

    print("🧠 DKF v17 SELF-HEALING OS LAYER ONLINE")

    state = load(STATE, {})
    memory = load(MEMORY, [])

    while True:
        if not ollama_alive():
            restart()

        q = input("DKF > ").strip()
        if q in ["exit", "quit"]:
            break

        context = ""
        for m in memory[-5:]:
            context += f"User: {m['u']}\nAI: {m['a']}\n"

        prompt = context + f"\nUser: {q}\nAI:"

        res = ask(prompt)

        memory.append({"u": q, "a": res})
        memory = memory[-50:]

        save(MEMORY, memory)
        save(STATE, state)

        print("\n🧠", res, "\n")
        print("-" * 60)


if __name__ == "__main__":
    run()
