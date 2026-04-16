# OMEGA EVENT BUS v4
# Backbone messaging system for Omega Core Stack v4

import time
import uuid
import json
import queue
import threading
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict

OMEGA_ROOT = Path(__file__).resolve().parent
LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# EVENT STRUCTURE
# =========================================================
@dataclass
class OmegaEvent:
    id: str
    type: str
    source: str
    payload: dict
    timestamp: float


def create_event(event_type, source, payload):
    return OmegaEvent(
        id=str(uuid.uuid4())[:8],
        type=event_type,
        source=source,
        payload=payload,
        timestamp=time.time()
    )


# =========================================================
# PERSISTENT EVENT LOG
# =========================================================
class EventLog:
    def __init__(self):
        self.file = LOG_DIR / "omega_event_bus.log"
        self.file.touch(exist_ok=True)

    def write(self, event: OmegaEvent):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(event)) + "\n")


# =========================================================
# EVENT BUS CORE
# =========================================================
class OmegaEventBusV4:
    """
    Central message backbone (ONLY communication layer)
    """

    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queue = queue.Queue()
        self.log = EventLog()
        self.running = False

    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)

    def publish(self, event: OmegaEvent):
        self.queue.put(event)

    def _dispatch(self, event: OmegaEvent):
        handlers = self.subscribers.get(event.type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"[Ω BUS v4] handler error: {e}")

    def start(self):
        self.running = True
        print("[Ω BUS v4] event backbone ONLINE")

        while self.running:
            try:
                event = self.queue.get(timeout=1)
                self.log.write(event)
                self._dispatch(event)

            except queue.Empty:
                continue
            except KeyboardInterrupt:
                print("\n[Ω BUS v4] shutdown signal")
                self.running = False


BUS = OmegaEventBusV4()


if __name__ == "__main__":

    def debug_handler(event):
        print(f"[EVENT] {event.type} | from {event.source} | {event.payload}")

    BUS.subscribe("test", debug_handler)
    BUS.start()
