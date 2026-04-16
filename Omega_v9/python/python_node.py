import json, time, random

BUS = "omega_v9_bus.json"

while True:
    msg = {
        "node": "python_worker",
        "confidence": random.random(),
        "reward": random.random(),
        "action": "explore"
    }

    with open(BUS, "w") as f:
        json.dump(msg, f)

    print("🐍 Python node active")
    time.sleep(0.4)
