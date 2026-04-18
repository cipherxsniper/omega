import json
import redis
import time

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MEMORY_KEY = "omega:memory"
INFLUENCE_KEY = "omega:influence"


def store_event(event, vector):
    payload = {
        "event": event,
        "vector": vector,
        "ts": time.time()
    }

    r.lpush(MEMORY_KEY, json.dumps(payload))
    r.ltrim(MEMORY_KEY, 0, 500)  # keep last 500 events


def load_memory(limit=200):
    raw = r.lrange(MEMORY_KEY, 0, limit)
    return [json.loads(x) for x in raw]


def update_influence(node, score):
    r.hset(INFLUENCE_KEY, node, score)


def get_influence_map():
    return r.hgetall(INFLUENCE_KEY)
