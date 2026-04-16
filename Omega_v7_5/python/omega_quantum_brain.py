import json
import random
import time

def generate():
    return {
        "type": "python_signal",
        "node": "py_core",
        "confidence": random.random(),
        "payload": {
            "analysis": random.random() * 100
        },
        "timestamp": time.time()
    }

while True:
    msg = generate()

    with open("../bus/python_signal.json", "w") as f:
        json.dump(msg, f)

    print("🐍 Python brain emitted signal")
    time.sleep(0.3)
