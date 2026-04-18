import redis
import time

_redis = None

def get_redis():
    global _redis

    if _redis:
        return _redis

    while True:
        try:
            _redis = redis.Redis(
                host="127.0.0.1",
                port=6379,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )

            _redis.ping()
            print("🟢 SAFE REDIS CONNECTED")
            return _redis

        except Exception as e:
            print("🔴 REDIS NOT READY - RETRYING...", e)
            time.sleep(2)
