class OmegaMessageBusV72:
    def __init__(self):
        self.subscribers = {}
        self.message_log = []

    def subscribe(self, node, handler):
        self.subscribers[node] = handler

    def publish(self, sender, target, payload):
        msg = {
            "from": sender,
            "to": target,
            "payload": payload
        }

        self.message_log.append(msg)

        if target in self.subscribers:
            return self.subscribers[target](payload)

        return None

    def broadcast(self, sender, payload):
        results = {}

        for node, handler in self.subscribers.items():
            if node != sender:
                results[node] = handler(payload)

        return results
