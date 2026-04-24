import requests
from model_patch import resolve_model

OLLAMA = "http://127.0.0.1:11434"

def ask(prompt):
    model = resolve_model()

    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()

while True:
    q = input("DKF > ")
    if q in ["exit", "quit"]:
        break

    print(ask(q))
