class OmegaTraceV76:
    """
    Standard execution trace format (EVERY node system must output this)
    """

    def __init__(self, path, final_node, steps, meta=None):
        self.path = path                  # list of visited nodes
        self.final_node = final_node     # string
        self.steps = steps                # int
        self.meta = meta or {}            # debug / stats


class OmegaFieldV76:
    """
    Shared system state (observer-safe structure)
    """

    def __init__(self, memory):
        self.global_memory = memory
        self.nodes = getattr(memory, "data", {}) if hasattr(memory, "data") else {}
        self.health = getattr(memory, "health", 0.5)


def normalize_trace(raw):
    """
    Converts ANY legacy trace format into v7.6 format
    """

    # dict-style (your current system)
    if isinstance(raw, dict):
        return OmegaTraceV76(
            path=raw.get("path", ["unknown"]),
            final_node=raw.get("final_node", "unknown"),
            steps=raw.get("steps", 0),
            meta=raw
        )

    # list-style fallback (older systems)
    if isinstance(raw, list):
        return OmegaTraceV76(
            path=[x.get("node", "unknown") for x in raw if isinstance(x, dict)],
            final_node=raw[-1].get("node", "unknown") if raw else "unknown",
            steps=len(raw),
            meta={}
        )

    return OmegaTraceV76(["unknown"], "unknown", 0, {})
