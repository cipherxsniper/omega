import time
from collections import deque

EVENTS = deque()

# ---------------------------
# ADD EVENT
# ---------------------------

def emit(event_type, payload):
    EVENTS.append({
        "type": event_type,
        "payload": payload,
        "time": time.time()
    })

# ---------------------------
# PROCESS EVENTS
# ---------------------------

def process():
    while EVENTS:
        event = EVENTS.popleft()

        print(f"[EVENT] {event['type']} -> {event['payload']}")

# ---------------------------
# LOOP
# ---------------------------

def run():
    while True:
        process()
        time.sleep(1)

if __name__ == "__main__":
    run()
