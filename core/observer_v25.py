import time
import traceback
import redis
from core.stream_safe import safe_xadd

STREAM = "omega.events"

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

print("🚀 OBSERVER_V25 ONLINE (STABLE STREAM ENGINE)")

def run_tick(i):
    data = {
        "type": "observer_tick",
        "tick": i,
        "status": "ok",
        "node": "observer_v25"
    }

    result = safe_xadd(r, STREAM, data)

    if result:
        print(f"🧠 OBSERVER_TICK OK {i}")
    else:
        print(f"⚠️ TICK DROPPED {i}")

def loop():
    i = 0

    while True:
        try:
            run_tick(i)
            i += 1

            # 🧠 CRITICAL: backpressure control
            time.sleep(0.2)

        except KeyboardInterrupt:
            print("🛑 CLEAN SHUTDOWN")
            break

        except Exception as e:
            print("⚠️ LOOP ERROR:", e)
            traceback.print_exc()
            time.sleep(1)

if __name__ == "__main__":
    loop()
