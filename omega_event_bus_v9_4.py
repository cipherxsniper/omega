# Ω EVENT BUS v9.4 — SYSTEMD STYLE MESSAGE LAYER

import time
from collections import deque

BUS = deque(maxlen=1000)

def publish(topic, data):
    BUS.append({"topic": topic, "data": data, "ts": time.time()})

def consume(topic):
    for msg in list(BUS):
        if msg["topic"] == topic:
            BUS.remove(msg)
            return msg["data"]
    return None

def stream(topic):
    while True:
        msg = consume(topic)
        if msg:
            yield msg
        time.sleep(0.05)
