class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def emit(self, event):
        # EVERY cognitive signal flows through here
        for sub in self.subscribers:
            sub(event)

bus = EventBus()

def emit(event):
    bus.emit(event)

def subscribe(fn):
    bus.subscribe(fn)
