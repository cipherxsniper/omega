import time
import traceback
import redis
from core.stream_safe import safe_xadd

STREAM = "omega.events"

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

print("🚀 OBSERVER V25 FIXED ONLINE")

def run_tick(i):
    try:
        data = {
            "type": "observer_tick",
            "tick": i,
            "status": "ok",
            "node": "observer_v25"
        }

        safe_xadd(r, STREAM, data)
        print("🧠 OBSERVER_TICK OK", i)

    except Exception as e:
        print("⚠️ OBSERVER ERROR:", e)
        traceback.print_exc()

def loop():
    i = 0
    while True:
        try:
            run_tick(i)
            i += 1
            time.sleep(0.2)   # IMPORTANT: prevents spin crash loop

        except KeyboardInterrupt:
            print("🛑 STOPPED CLEANLY")
            break

        except Exception as e:
            print("⚠️ LOOP ERROR:", e)
            time.sleep(1)

if __name__ == "__main__":
    loop()
