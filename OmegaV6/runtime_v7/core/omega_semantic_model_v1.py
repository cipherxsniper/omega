from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SemanticModelV1:

    def __init__(self):
        self.crdt = get_crdt()

    # -------------------------
    # EVENT → MEANING
    # -------------------------
    def interpret(self, event):
        etype = event.get("type", "unknown")

        if etype == "heartbeat":
            return {
                "entity": "system",
                "state": "alive",
                "confidence": 0.9
            }

        if etype == "ping":
            return {
                "entity": "node",
                "state": "communicating",
                "confidence": 0.8
            }

        return {
            "entity": "unknown_event",
            "state": "unclassified_pattern",
            "confidence": 0.4
        }

    # -------------------------
    # BUILD WORLD VIEW
    # -------------------------
    def world_state(self):
        events = self.crdt.get_events()
        return [self.interpret(e) for e in events[-50:]]
