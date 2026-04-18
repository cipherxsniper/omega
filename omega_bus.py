# 🧠 OMEGA UNIFIED BUS v2 (COMPATIBLE CORE)

import time

class OmegaBus:
    def __init__(self):
        self.history = []
        self.subscribers = {}

    # 🔁 WRITE EVENT
    def publish(self, topic, data):
        event = {
            "topic": topic,
            "data": data,
            "timestamp": time.time()
        }

        self.history.append(event)

        # notify subscribers
        if topic in self.subscribers:
            for fn in self.subscribers[topic]:
                try:
                    fn(event)
                except Exception as e:
                    print(f"[BUS ERROR] {e}")

    # 👂 SUBSCRIBE TO EVENTS
    def subscribe(self, topic, fn):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(fn)

    # 📖 READ BUFFER (THIS FIXES YOUR CRASH)
    def read(self):
        return self.history

    # 🧠 OPTIONAL: FILTERED READ
    def read_topic(self, topic):
        return [e for e in self.history if e["topic"] == topic]


# GLOBAL BUS INSTANCE
BUS = OmegaBus()
