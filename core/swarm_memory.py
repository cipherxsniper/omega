import json
import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MEMORY_KEY = "omega:swarm:memory"


def store(event, vector):
    data = {
        "event": json.dumps(event),
        "vector": json.dumps(vector)
    }
    r.rpush(MEMORY_KEY, json.dumps(data))


def load_all(limit=500):
    items = r.lrange(MEMORY_KEY, -limit, -1)

    memory = []
    for i in items:
        try:
            obj = json.loads(i)
            memory.append({
                "event": json.loads(obj["event"]),
                "vector": json.loads(obj["vector"])
            })
        except:
            continue

    return memory
