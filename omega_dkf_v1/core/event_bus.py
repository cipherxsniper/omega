class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event, fn):
        self.subscribers.setdefault(event, []).append(fn)

    def emit(self, event, data):
        for fn in self.subscribers.get(event, []):
            fn(data)
