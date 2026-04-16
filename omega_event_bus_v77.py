class OmegaEventBusV77:
    def __init__(self):
        self.subscribers = {}
        self.history = []

    def subscribe(self, event_type, fn):
        self.subscribers.setdefault(event_type, []).append(fn)

    def emit(self, event):
        self.history.append(event)

        for fn in self.subscribers.get(event["type"], []):
            event = fn(event)

        return event
