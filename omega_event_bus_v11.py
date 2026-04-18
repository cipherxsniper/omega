import redis
import json
import time

r = redis.Redis()

CHANNEL = "omega.events"

def emit(event_type, node, data=None):
    event = {
        "type": event_type,
        "node": node,
        "data": data or {},
        "timestamp": time.time()
    }

    r.publish(CHANNEL, json.dumps(event))
    return event
