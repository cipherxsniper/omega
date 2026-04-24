import requests
from dkf_auto_model_resolver import get_model

OLLAMA = "http://127.0.0.1:11434"

def chat(prompt):
    model = get_model()

    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json().get("response", "")


print("🧠 DKF CORE RUNNER ONLINE")

while True:
    q = input("DKF > ").strip()
    if q in ["exit", "quit"]:
        break

    print(chat(q))
