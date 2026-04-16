from collections import defaultdict, deque

class OmegaEventBusV716:

    def __init__(self, maxlen=1000):
        self.subscribers = defaultdict(list)
        self.stream = deque(maxlen=maxlen)

    def publish(self, event):
        self.stream.append(event)

        event_type = event.get("event_type", "unknown")

        for fn in self.subscribers[event_type]:
            try:
                fn(event)
            except Exception as e:
                # bus NEVER crashes system
                print(f"[Ω BUS ERROR] {e}", flush=True)

    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)

    def history(self):
        return list(self.stream)
