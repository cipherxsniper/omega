import redis
import time
import uuid

# 🔑 CONFIG
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

LEADER_KEY = "omega.leader"
LEADER_TTL = 3  # seconds

NODE_ID = f"node_{uuid.uuid4().hex[:6]}"

print("🧠 STARTING OBSERVER_V26 NODE")

# 🔌 CONNECT (auto-retry)
def connect_redis():
    while True:
        try:
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            r.ping()
            print(f"✅ Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return r
        except Exception:
            print("⏳ Waiting for Redis...")
            time.sleep(1)

# 🧠 LEADER ELECTION
def is_leader(r, node_id):
    try:
        current = r.get("omega.leader")
        
        if current is None:
            if r.set("omega.leader", node_id, nx=True, ex=3):
                return True
        
        if current == node_id:
            r.expire("omega.leader", 3)
            return True
        
        ttl = r.ttl("omega.leader")
        if ttl == -1 or ttl == -2:
            if r.set("omega.leader", node_id, ex=3):
                return True
        
        return False
    except Exception as e:
        print("⚠️ leader error:", e)
        return False

    except Exception as e:
        print("⚠️ Leader check error:", e)
        return False

# 🧠 WORK
def run_tick(tick):
    print(f"🔥 processing tick {tick}")

# 🚀 MAIN LOOP
def main():
    r = connect_redis()
    tick = 0

    print(f"🚀 OBSERVER_V26 ONLINE | NODE={NODE_ID}")

    while True:
        if is_leader(r, NODE_ID):
            print(f"🧠 [{NODE_ID}] LEADER TICK {tick}")
            run_tick(tick)
            tick += 1
        else:
            print(f"⏸️ [{NODE_ID}] standby (leader active)")

        time.sleep(0.2)  # stabilize loop
        time.sleep(0.05) # prevent race condition

if __name__ == "__main__":
    main()
