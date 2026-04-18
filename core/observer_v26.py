import time
import uuid
import redis
import traceback
from core.connection_manager import get_connection
from core.stream_safe import safe_xadd

STREAM = "omega.events"

# 🧠 UNIQUE NODE ID
NODE_ID = f"node_{uuid.uuid4().hex[:6]}"

# 🧠 LEADER LOCK CONFIG
LEADER_KEY = "omega.leader"
LEADER_TTL = 3  # seconds

# 🔌 CONNECT (AUTO-RECOVER)
r = get_connection()

print(f"🚀 OBSERVER_V26 ONLINE | NODE={NODE_ID}")

def is_leader(r, node_id):
    try:
        # try to become leader
        if r.set(LEADER_KEY, node_id, nx=True, ex=LEADER_TTL):
            return True

        # check current leader
        leader = r.get(LEADER_KEY)

        if leader == node_id:
            # refresh leadership
            r.expire(LEADER_KEY, LEADER_TTL)
            return True

        return False

    except Exception as e:
        print("⚠️ Leader check error:", e)
        return False


def ensure_connection(r):
    try:
        r.ping()
        return r
    except:
        print("⚠️ Redis connection lost — reconnecting...")
        return get_connection()


def run_tick(tick):
    try:
        data = {
            "type": "observer_tick",
            "tick": tick,
            "node": NODE_ID,
            "status": "leader"
        }

        safe_xadd(r, STREAM, data)

    except Exception as e:
        print("⚠️ TICK ERROR:", e)
        traceback.print_exc()


def loop():
    tick = 0

    while True:
        try:
            # 🔌 ensure Redis alive
            global r
            r = ensure_connection(r)

            # 🧠 LEADER LOGIC
            if is_leader(r, NODE_ID):
                print(f"🧠 [{NODE_ID}] LEADER TICK {tick}")
                run_tick(tick)
                tick += 1
            else:
                print(f"⏸️ [{NODE_ID}] standby (leader active)")

            # 🧠 anti race / CPU burn
            time.sleep(0.2)

        except KeyboardInterrupt:
            print("🛑 STOPPED CLEANLY")
            break

        except Exception as e:
            print("⚠️ LOOP ERROR:", e)
            time.sleep(1)


if __name__ == "__main__":
    loop()
