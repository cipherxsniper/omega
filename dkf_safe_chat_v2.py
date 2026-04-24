import requests
import time

MODEL = "tinyllama:latest"

def ask(prompt):
    for attempt in range(3):
        try:
            r = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            return r.json().get("response", "[no response]")
        except Exception as e:
            print(f"⚠️ retry {attempt+1}/3 failed:", e)
            time.sleep(2)
    return "❌ failed after retries"

print("🧠 DKF SAFE CHAT v2 ONLINE")

while True:
    q = input("DKF > ").strip()
    if q in ["exit","quit"]:
        break

    print("\n🧠 RESPONSE:\n")
    print(ask(q))
    print("\n" + "-"*50 + "\n")
