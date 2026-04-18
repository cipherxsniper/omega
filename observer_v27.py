import redis
import time
import uuid
import json
import random

NODE_ID = f"node_{uuid.uuid4().hex[:6]}"

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

STREAM_THOUGHTS = "omega.thoughts"

print(f"🧠 OBSERVER_V27 MESH ONLINE | {NODE_ID}")

# 🧠 generate "brain signal"
def think(tick):
    return {
        "node": NODE_ID,
        "tick": tick,
        "signal": random.random(),
        "intent": random.choice(["analyze", "observe", "predict", "sync"])
    }

# 🧠 publish thought
def publish(thought):
    r.xadd(STREAM_THOUGHTS, thought)

# 🧠 read global thoughts
def read_thoughts():
    data = r.xrange(STREAM_THOUGHTS, min='-', max='+', count=20)
    return [eval(item[1]) for item in data if item]

# 🧠 consensus engine
def consensus(thoughts):
    if not thoughts:
        return 0

    signals = [t["signal"] for t in thoughts]
    return sum(signals) / len(signals)

tick = 0

while True:
    # 1. think
    my_thought = think(tick)
    publish(my_thought)

    # 2. read global mind
    thoughts = read_thoughts()

    # 3. compute shared cognition
    avg = consensus(thoughts)

    # 4. act based on mesh state
    if avg > 0.6:
        print(f"🔥 [{NODE_ID}] HIGH MESH ACTIVITY tick={tick} avg={avg:.3f}")
    else:
        print(f"🧠 [{NODE_ID}] stable mesh tick={tick} avg={avg:.3f}")

    tick += 1
    time.sleep(0.2)
