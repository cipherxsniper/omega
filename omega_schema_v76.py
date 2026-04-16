class OmegaSchemaV76:

    @staticmethod
    def tick(node, state, trace, memory, events, tick_id):
        return {
            "tick": tick_id,
            "node": node,
            "state": state or {},
            "trace": trace or [],
            "memory": memory or {},
            "events": events or []
        }

    @staticmethod
    def validate(tick_obj):
        required = ["tick", "node", "state", "trace", "memory", "events"]
        for k in required:
            if k not in tick_obj:
                raise Exception(f"[SCHEMA ERROR] Missing field: {k}")
        return True
