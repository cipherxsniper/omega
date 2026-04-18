# 🧠 Omega v11.5 Event Bus (Cross-Node Communication Layer)

import time
from collections import defaultdict, deque

class EventBus:

    def __init__(self):
        self.subscribers = defaultdict(list)
        self.event_log = deque(maxlen=500)

    # subscribe node to event type
    def subscribe(self, event_type, node):
        self.subscribers[event_type].append(node)

    # publish event into ecosystem
    def publish(self, event_type, source, payload):

        event = {
            "type": event_type,
            "source": source,
            "payload": payload,
            "timestamp": time.time()
        }

        self.event_log.append(event)

        # fan-out to subscribers
        for node in self.subscribers[event_type]:

            if node != source:
                self.dispatch(node, event)

        return event

    # dispatch event to node (logical injection)
    def dispatch(self, node, event):
        # In real system this would call node.step()
        # Here we simulate ingestion hook
        print(f"[EVENT] {event['source']} → {node} | {event['type']}")

    def get_recent(self):
        return list(self.event_log)
