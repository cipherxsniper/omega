import requests

r = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={
        "model": "tinyllama:latest",
        "prompt": "say hello",
        "stream": False
    }
)

print(r.json())
