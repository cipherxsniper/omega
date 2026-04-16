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

# === COMPAT PATCH: normalize_trace (v7.6 fallback) ===
def normalize_trace(trace):
    """
    Safe fallback normalizer so observer never crashes.
    """
    if trace is None:
        return []

    if isinstance(trace, dict):
        return [{"node": trace.get("final_node", "unknown"), "data": trace}]

    if isinstance(trace, list):
        return trace

    return [{"node": str(trace), "data": trace}]

