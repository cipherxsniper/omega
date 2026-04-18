import time
import traceback
import redis
import signal
import sys

# =========================
# REDIS CONFIG
# =========================
STREAM_KEY = "omega.events"
GROUP = "observer_group"
CONSUMER = "observer_v24"

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

running = True

# =========================
# CLEAN SHUTDOWN HANDLER
# =========================
def shutdown(sig, frame):
    global running
    print("\n🛑 OBSERVER SHUTDOWN REQUESTED")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# =========================
# GROUP INIT (SAFE)
# =========================
def ensure_group():
    try:
        r.xgroup_create(STREAM_KEY, GROUP, id="0", mkstream=True)
        print("🧠 STREAM GROUP CREATED")
    except Exception:
        # already exists
        pass

# =========================
# EVENT HANDLER
# =========================
def handle_event(event_id, data):
    try:
        print(f"🧠 EVENT RECEIVED: {event_id} | {data}")

        # Example processing logic (expand later)
        # store metrics, route to swarm, etc.

    except Exception as e:
        print("⚠️ EVENT ERROR:", e)
        traceback.print_exc()

# =========================
# MAIN LOOP (STREAM CONSUMER)
# =========================
def run():
    ensure_group()

    last_id = "0"

    print("🚀 OBSERVER_V25 ONLINE (Redis Stream Mode)")

    while running:
        try:
            response = r.xreadgroup(
                GROUP,
                CONSUMER,
                {STREAM_KEY: ">"},
                count=10,
                block=5000
            )

            if not response:
                continue

            for stream, messages in response:
                for msg_id, data in messages:
                    handle_event(msg_id, data)

                    # ACK (prevents reprocessing)
                    r.xack(STREAM_KEY, GROUP, msg_id)

        except Exception as e:
            print("⚠️ STREAM ERROR:", e)
            traceback.print_exc()
            time.sleep(2)

# =========================
# BOOT
# =========================
if __name__ == "__main__":
    run()
