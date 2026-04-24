import requests
import json

print("🧠 DKF DEBUG TEST START")

try:
    r = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "tinyllama:latest",
            "prompt": "hello",
            "stream": False
        },
        timeout=30
    )

    print("STATUS:", r.status_code)
    print("RAW:", r.text)

    try:
        print("JSON:", r.json())
    except Exception as e:
        print("JSON PARSE ERROR:", e)

except Exception as e:
    print("REQUEST FAILED:", e)
