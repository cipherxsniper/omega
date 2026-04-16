class UCPV79:

    @staticmethod
    def build(tick, node, trace, state, memory, events):
        return {
            "tick": int(tick),
            "node": str(node),
            "trace": trace if isinstance(trace, list) else [],
            "state": state if isinstance(state, dict) else {},
            "memory": memory if isinstance(memory, dict) else {},
            "events": events if isinstance(events, list) else []
        }

    @staticmethod
    def validate(packet):
        required = ["tick", "node", "trace", "state", "memory", "events"]

        for k in required:
            if k not in packet:
                raise Exception(f"[UCP ERROR] Missing field: {k}")

        return True
