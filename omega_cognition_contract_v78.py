class CognitionPacketV78:
    """
    Single universal data contract for ALL Omega subsystems.
    """

    def __init__(self, tick, node, state, trace, memory, events):
        self.tick = tick
        self.node = node
        self.state = state or {}
        self.trace = trace or []
        self.memory = memory or {}
        self.events = events or []

    def to_dict(self):
        return {
            "tick": self.tick,
            "node": self.node,
            "state": self.state,
            "trace": self.trace,
            "memory": self.memory,
            "events": self.events
        }

    @staticmethod
    def validate(obj):
        required = ["tick", "node", "state", "trace", "memory", "events"]
        for k in required:
            if k not in obj:
                raise Exception(f"[V78 CONTRACT VIOLATION] Missing: {k}")
        return True
