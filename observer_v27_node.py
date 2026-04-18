import redis
import time
import uuid
import os
import random

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

NODE_ID = os.getenv("NODE_ID", f"node_{uuid.uuid4().hex[:6]}")

print(f"🧠 NODE ONLINE | {NODE_ID}")

STREAM = "omega.thoughts"

# register node
r.sadd("omega.nodes", NODE_ID)

def think():
    return random.random()

while True:
    # 🧠 generate signal
    signal = think()

    # store node state
    r.set(f"omega.signal.{NODE_ID}", signal)

    # publish to shared brain stream
    r.xadd(STREAM, {
        "node": NODE_ID,
        "signal": signal
    })

    # read swarm context
    others = r.xrange(STREAM, min='-', max='+', count=10)

    if signal > 0.7:
        print(f"🔥 [{NODE_ID}] HIGH ACTIVITY {signal:.3f}")
    else:
        print(f"🧠 [{NODE_ID}] stable {signal:.3f}")

    time.sleep(0.5)
