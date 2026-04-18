import os
import time
import random
import json
import redis

NODE_ID = os.getenv("NODE_ID", "node-default")

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

print("🟢 NODE ONLINE:", NODE_ID)

while True:
    event = {
        "node": NODE_ID,
        "type": "heartbeat",
        "payload": {
            "cpu": random.random(),
            "memory": random.random(),
            "load": random.random()
        },
        "timestamp": time.time()
    }

    r.publish("omega.events", json.dumps(event))
    print("📡 EVENT:", NODE_ID)

    time.sleep(2)
