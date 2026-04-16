import time
import json
import random
import redis

r = redis.Redis()

NODE_ID = "python-node-1"

while True:
    heartbeat = {
        "node": NODE_ID,
        "type": "heartbeat",
        "cpu": random.random(),
        "memory": random.random(),
        "timestamp": time.time()
    }

    r.publish("omega.heartbeat", json.dumps(heartbeat))

    print("🐍 HEARTBEAT:", heartbeat)

    time.sleep(3)
