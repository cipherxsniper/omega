import time
import json
import os

FILE = "../bus/omega_message.json"

def process(msg):
    print("🐍 Python received:", msg["type"])

    # learning simulation
    if msg["payload"].get("action") == "learn":
        msg["learning_result"] = {
            "adjustment": msg["payload"]["value"] * 1.1
        }

    return msg

while True:
    if os.path.exists(FILE):
        with open(FILE) as f:
            try:
                msg = json.load(f)
                updated = process(msg)

                with open(FILE, "w") as fw:
                    json.dump(updated, fw, indent=2)

            except Exception as e:
                print("error:", e)

    time.sleep(1)
