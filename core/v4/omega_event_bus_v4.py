import time
import threading
from queue import Queue

class EventBusV4:
    def __init__(self):
        self.queue = Queue()
        self.subs = []

    def emit(self, event_type, payload=None):
        self.queue.put({
            "type": event_type,
            "payload": payload,
            "ts": time.time()
        })

    def subscribe(self, fn):
        self.subs.append(fn)

    def start(self):
        def loop():
            while True:
                event = self.queue.get()
                for s in self.subs:
                    try:
                        s(event)
                    except Exception as e:
                        print("[BUS v4 ERROR]", e)

        threading.Thread(target=loop, daemon=True).start()

BUS = EventBusV4()
