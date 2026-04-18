import redis
import time
import traceback
import random

def log(msg):
    print(msg, flush=True)

# =====================
# SAFE REDIS CONNECT
# =====================
while True:
    try:
        r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
        r.ping()
        log("🧠 Redis ONLINE")
        break
    except Exception as e:
        log(f"⏳ Redis retry: {e}")
        time.sleep(1)

# =====================
# MAIN LOOP (SAFE)
# =====================
tick = 0

while True:
    try:
        nodes = r.smembers("omega.nodes")
        r.set("omega.node_count", len(nodes))

        signals = []
        for n in nodes:
            v = r.get(f"omega.signal.{n}")
            if v:
                signals.append(float(v))

        if signals:
            if "prev_avg" not in globals():
    prev_avg = 0

raw_avg = sum(signals) / len(signals)

avg = 0.2 * raw_avg + 0.8 * prev_avg
prev_avg = avg
            log(f"🌐 SWARM COGNITION AVG = {avg:.3f}")

        log(f"📊 Active nodes: {len(nodes)} | tick={tick}")

        tick += 1
        time.sleep(2)

    except Exception as e:
        log("🔥 BRAIN ERROR:")
        log(traceback.format_exc())
        time.sleep(2)
