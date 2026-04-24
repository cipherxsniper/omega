import requests

MODEL = "tinyllama:latest"

print("🧠 DKF SAFE CHAT ONLINE")

while True:
    q = input("DKF > ").strip()

    if q in ["exit", "quit"]:
        break

    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": q,
                "stream": False
            },
            timeout=30
        )

        data = r.json()
        print("\n🧠 RESPONSE:\n")
        print(data.get("response", "[NO RESPONSE]"))
        print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print("❌ ERROR:", e)
