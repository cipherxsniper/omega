class OmegaEventBusV77:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(event)

    def broadcast(self):
        return self.events[-50:]

    def filter(self, event_type):
        return [e for e in self.events if e["type"] == event_type]
