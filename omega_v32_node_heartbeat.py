import redis
import time

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

def heartbeat(node_id):
    while True:
        r.set(f"omega.nodes.heartbeat.{node_id}", 1, ex=5)
        time.sleep(1)
