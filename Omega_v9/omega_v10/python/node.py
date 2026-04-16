import redis
import json
import time
import random

r = redis.Redis()

print("🐍 Python Worker ONLINE")

while True:
    msg = {
        "node": "python_worker",
        "confidence": random.random(),
        "reward": random.random(),
        "action": "explore"
    }

    r.publish("omega_stream", json.dumps(msg))
    time.sleep(0.4)
