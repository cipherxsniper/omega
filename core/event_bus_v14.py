import redis, json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

CHANNEL = "omega.events"

def publish(event):
    r.publish(CHANNEL, json.dumps(event))

def subscribe(callback):
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)

    for msg in pubsub.listen():
        if msg["type"] == "message":
            callback(json.loads(msg["data"]))
