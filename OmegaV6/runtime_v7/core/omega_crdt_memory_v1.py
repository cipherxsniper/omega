import time
import hashlib
import json
import threading


class CRDTMemoryV1:
    """
    Conflict-free Replicated Data Store (simplified Omega version)
    """

    def __init__(self, path="memory/omega_crdt_v1.json"):
        self.path = path
        self.lock = threading.Lock()

        self.state = {
            "events": [],
            "nodes": {},
            "meta": {
                "version": "CRDT_V1",
                "last_update": time.time()
            }
        }

        self.load()

    # -------------------------
    # HASH IDENTITY
    # -------------------------
    def hash_event(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    # -------------------------
    # APPLY EVENT (CRDT SAFE)
    # -------------------------
    def apply(self, event):
        with self.lock:
            event_id = self.hash_event(event)

            # prevent duplicates
            if any(e.get("_id") == event_id for e in self.state["events"]):
                return

            event["_id"] = event_id
            event["_ts"] = time.time()

            self.state["events"].append(event)

            # bounded memory
            if len(self.state["events"]) > 5000:
                self.state["events"] = self.state["events"][-2500:]

            self.state["meta"]["last_update"] = time.time()
            self.save()

    # -------------------------
    # MERGE (CRDT CORE)
    # -------------------------
    def merge(self, incoming_events):
        for e in incoming_events:
            self.apply(e)

    # -------------------------
    # LOAD / SAVE
    # -------------------------
    def load(self):
        try:
            with open(self.path, "r") as f:
                self.state = json.load(f)
        except:
            pass

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    # -------------------------
    # ACCESSOR
    # -------------------------
    def get_events(self):
        return self.state["events"]


_global_crdt = None


def get_crdt():
    global _global_crdt
    if _global_crdt is None:
        _global_crdt = CRDTMemoryV1()
    return _global_crdt
