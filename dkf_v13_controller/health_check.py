import requests

try:
    r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
    print("🟢 Ollama is ACTIVE")
    print(r.json())
except:
    print("🔴 Ollama is OFFLINE")
