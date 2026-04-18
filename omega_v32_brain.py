import time
import redis

print("🧠 BRAIN BOOTING...")

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# SAFE IMPORT
try:
    import omega_v32_adaptive_core as core
    print("🧠 CORE OK")
except Exception as e:
    print("❌ CORE IMPORT FAILED:", e)
    core = None

NODE_ID = f"node_{int(time.time()) % 100000}"
tick = 0

while True:
    try:
        val = 0.4 + ((tick % 5) * 0.02)

        print(f"🧠 {NODE_ID} tick={tick} signal={val}")

        tick += 1
        time.sleep(1)

    except Exception as e:
        print("⚠️ LOOP ERROR:", e)
        time.sleep(1)
