import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

TARGET = 24

def real_node_count():
    return len(r.smembers("omega.nodes.active"))


def watchdog_tick():
    count = real_node_count()

    if count < TARGET:
        print(f"⚠️ REAL node deficit detected: {count}/{TARGET}")
    else:
        print(f"✅ Mesh stable: {count}/{TARGET}")
