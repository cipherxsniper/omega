from collections import defaultdict, deque

class OmegaMessageBusV74:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queue = deque()
        self.history = []

    def publish(self, event):
        self.queue.append(event)

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

    def dispatch(self):
        if not self.queue:
            return

        event = self.queue.popleft()
        self.history.append(event)

        handlers = self.subscribers.get(event["type"], [])

        results = []
        for h in handlers:
            try:
                results.append(h(event))
            except Exception as e:
                results.append({"error": str(e)})

        return results
