# OMEGA EVENT ROUTER v1
# Lightweight message bus for all Omega subsystems

import time
from collections import deque
from threading import Lock


class EventRouter:
    def __init__(self):
        self.events = deque(maxlen=1000)
        self.lock = Lock()

    def emit(self, event_type, payload=None):
        with self.lock:
            event = {
                "type": event_type,
                "payload": payload,
                "ts": time.time()
            }
            self.events.append(event)

    def get_events(self, event_type=None):
        with self.lock:
            if event_type:
                return [e for e in self.events if e["type"] == event_type]
            return list(self.events)


ROUTER = EventRouter()
