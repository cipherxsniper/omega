# ============================================================
# OMEGA EVENT MESH v5 — GLOBAL INTELLIGENCE BUS
# Connects ALL scripts into one shared cognition network
# ============================================================

import time
from collections import defaultdict


# ============================================================
# 🌐 GLOBAL EVENT MESH (SHARED ACROSS SYSTEM)
# ============================================================

class OmegaEventMesh:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.subscribers = defaultdict(list)
        self.global_event_log = []

    # --------------------------------------------------------
    # SUBSCRIBE TO GLOBAL EVENTS
    # --------------------------------------------------------

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

    # --------------------------------------------------------
    # PUBLISH GLOBAL EVENTS
    # --------------------------------------------------------

    def publish(self, event_type, data=None, source="unknown"):
        event = {
            "type": event_type,
            "data": data,
            "source": source,
            "timestamp": time.time()
        }

        self.global_event_log.append(event)

        for handler in self.subscribers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"[MESH ERROR] {event_type}: {e}")

    # --------------------------------------------------------
    # GET EVENT HISTORY
    # --------------------------------------------------------

    def history(self, event_type=None):
        if event_type:
            return [e for e in self.global_event_log if e["type"] == event_type]
        return self.global_event_log
