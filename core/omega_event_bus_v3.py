import json
import time
import threading
from queue import Queue

class EventBusV3:
    def __init__(self):
        self.queue = Queue()
        self.subscribers = []

    def emit(self, event_type, payload=None):
        self.queue.put({
            "type": event_type,
            "payload": payload,
            "ts": time.time()
        })

    def subscribe(self, handler):
        self.subscribers.append(handler)

    def start(self):
        def loop():
            while True:
                event = self.queue.get()
                for h in self.subscribers:
                    try:
                        h(event)
                    except Exception as e:
                        print("[BUS ERROR]", e)

        threading.Thread(target=loop, daemon=True).start()

BUS = EventBusV3()
