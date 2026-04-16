import json
import time
import random

FILE = "../bus/omega_message.json"

while True:
    msg = {
        "type": "python_worker_signal",
        "from": "python_worker",
        "to": "node_core",
        "payload": {
            "confidence": random.random(),
            "decision": random.choice(["explore", "exploit"])
        },
        "timestamp": time.time()
    }

    with open(FILE, "w") as f:
        json.dump(msg, f, indent=2)

    print("🐍 Python worker sent signal")
    time.sleep(4)
