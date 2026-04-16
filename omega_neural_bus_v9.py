import time
import threading
from collections import defaultdict, deque

class NeuralBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queue = deque()
        self.running = True

    # -------------------------
    # SUBSCRIBE
    # -------------------------
    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)

    # -------------------------
    # PUBLISH
    # -------------------------
    def publish(self, event_type, data):
        self.queue.append((event_type, data))

    # -------------------------
    # DISPATCH LOOP
    # -------------------------
    def _loop(self):
        while self.running:
            if self.queue:
                event_type, data = self.queue.popleft()

                for cb in self.subscribers.get(event_type, []):
                    try:
                        cb(data)
                    except Exception as e:
                        print("[Ω BUS ERROR]", e)

            time.sleep(0.02)

    # -------------------------
    # START
    # -------------------------
    def start(self):
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()
        return t


# GLOBAL BUS INSTANCE (SAFE)
BUS = NeuralBus()
BUS.start()
