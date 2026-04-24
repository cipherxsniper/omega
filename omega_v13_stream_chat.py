import requests
import sys
import json

OLLAMA_URL = "http://127.0.0.1:11434"

# -----------------------------
# MODEL RESOLVER (simple safe fallback)
# -----------------------------
def resolve_model():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = r.json().get("models", [])

        if not models:
            return "tinyllama:latest"

        # prefer smallest model automatically
        for m in models:
            name = m.get("name", "")
            if "tiny" in name.lower():
                return name

        return models[0].get("name", "tinyllama:latest")

    except:
        return "tinyllama:latest"


# -----------------------------
# SYSTEM CONTEXT (this fixes “random personality drift”)
# -----------------------------
SYSTEM_PROMPT = """You are Omega, a stable AI reasoning system.
You are not roleplaying unless asked.
You respond clearly, technically, and directly.
You can ask questions back to improve understanding.
"""


# -----------------------------
# STREAM ENGINE
# -----------------------------
def stream_generate(prompt):
    model = resolve_model()

    payload = {
        "model": model,
        "prompt": SYSTEM_PROMPT + "\nUser: " + prompt + "\nOmega:",
        "stream": True
    }

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=60
        )

        print("\n🧠 RESPONSE:\n")

        for line in r.iter_lines():
            if not line:
                continue

            try:
                chunk = json.loads(line.decode("utf-8"))
                token = chunk.get("response", "")

                sys.stdout.write(token)
                sys.stdout.flush()

                if chunk.get("done"):
                    break

            except:
                continue

        print("\n")

    except Exception as e:
        print(f"\n[DKF STREAM ERROR] {e}\n")


# -----------------------------
# MAIN LOOP
# -----------------------------
print("🧠 DKF STREAM ENGINE v13 ONLINE")

while True:
    try:
        q = input("Ω > ").strip()

        if q in ["exit", "quit"]:
            break

        if not q:
            continue

        stream_generate(q)
        print("-" * 50)

    except KeyboardInterrupt:
        print("\n🧠 shutdown")
        break
