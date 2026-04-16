subscribers = {}

def subscribe(event, fn):
    subscribers.setdefault(event, []).append(fn)

def publish(event, data):
    for fn in subscribers.get(event, []):
        fn(data)
