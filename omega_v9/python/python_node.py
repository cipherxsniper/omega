import json
import time
import random

BUS = "omega_v9_bus.json"

while True:
    msg = {
        "node": "python_worker",
        "confidence": random.random(),
        "reward_signal": random.choice([0.1, -0.1, 0.3]),
        "action": random.choice(["explore", "exploit"])
    }

    with open(BUS, "w") as f:
        json.dump(msg, f)

    print("🐍 Python node emitted")
    time.sleep(0.4)
