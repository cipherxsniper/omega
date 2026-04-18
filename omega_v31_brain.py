import time
import redis
from omega_v31_consensus_core import vote, compute

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

NODE_ID = f"node_{int(time.time()) % 100000}"

r.sadd("omega.nodes.active", NODE_ID)
r.set(f"omega.nodes.weight.{NODE_ID}", 1.0)

tick = 0


def signal():
    # simulated intelligence signal (replace with real model later)
    return 0.4 + (tick % 10) * 0.01


while True:
    val = signal()

    vote(tick, NODE_ID, val)

    consensus, stability = compute(tick)

    print(f"🧠 NODE {NODE_ID}")
    print(f"🌐 CONSENSUS = {consensus:.3f}")
    print(f"📊 STABILITY = {stability:.3f}")
    print(f"📌 TICK = {tick}\n")

    tick += 1
    time.sleep(1)
