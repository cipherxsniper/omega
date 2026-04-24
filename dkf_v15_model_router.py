import requests

OLLAMA = "http://127.0.0.1:11434"

def resolve_model():
    try:
        r = requests.get(f"{OLLAMA}/api/tags", timeout=5)
        models = r.json().get("models", [])

        if not models:
            return "tinyllama:latest"

        for m in models:
            if "tiny" in m.get("name", ""):
                return m["name"]

        return models[0]["name"]

    except:
        return "tinyllama:latest"
