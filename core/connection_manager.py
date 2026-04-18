import redis
import time

CANDIDATES = [
    ("127.0.0.1", 6379),
    ("localhost", 6379),
]

def find_best_connection():
    for host, port in CANDIDATES:
        try:
            r = redis.Redis(host=host, port=port, decode_responses=True)
            if r.ping():
                print(f"✅ Connected to Redis at {host}:{port}")
                return r
        except Exception:
            continue

    print("⚠️ No Redis connection found, retrying...")
    time.sleep(1)
    return None


def get_connection():
    r = None
    while r is None:
        r = find_best_connection()
    return r
