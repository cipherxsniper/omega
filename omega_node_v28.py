import redis
import time
import uuid
import os
import random

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

NODE_ID = os.getenv("NODE_ID", f"node_{uuid.uuid4().hex[:6]}")

r.sadd("omega.nodes", NODE_ID)

print(f"[NODE] [{NODE_ID}] online")

while True:
    signal = random.random()

    r.set(f"omega.signal.{NODE_ID}", signal)

    if signal > 0.75:
        print(f"[NODE] [{NODE_ID}] HIGH signal={signal:.3f}")
    else:
        print(f"[NODE] [{NODE_ID}] stable signal={signal:.3f}")

    time.sleep(0.5)
