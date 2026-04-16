import redis
import json
import time
import numpy as np

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def process(msg):
    msg = json.loads(msg)

    confidence = msg.get("confidence", 0)

    reward = np.tanh(confidence * 2)

    return {
        "type": "python_response",
        "origin": msg["id"],
        "reward": float(reward),
        "suggestion": "explore" if reward > 0.5 else "exploit"
    }

pubsub = r.pubsub()
pubsub.subscribe("omega_stream")

print("🐍 Python Omega Brain ONLINE")

for message in pubsub.listen():
    if message["type"] == "message":
        response = process(message["data"])
        r.publish("omega_feedback", json.dumps(response))
