class OmegaSelfModelV78:
    def __init__(self):
        self.last_snapshot = None

    def snapshot(self, layer, trace, tick):
        return {
            "tick": tick,
            "final_node": trace.get("final_node"),
            "trace": trace,
            "memory_keys": list(getattr(layer.memory, "__dict__", layer.memory).keys())
        }

    def compare(self, prev, curr):
        if not prev:
            return "Initial system activation detected."

        changes = []

        if prev["final_node"] != curr["final_node"]:
            changes.append(
                f"Node transition: {prev['final_node']} → {curr['final_node']}"
            )

        if len(curr["memory_keys"]) != len(prev["memory_keys"]):
            changes.append("Memory structure changed.")

        return "; ".join(changes) if changes else "No structural changes detected."

    def narrate(self, prev, curr):
        delta = self.compare(prev, curr)

        return (
            f"[SELF-MODEL REPORT]\n"
            f"Tick: {curr['tick']}\n"
            f"Active node: {curr['final_node']}\n"
            f"System delta: {delta}\n"
            f"Meta-question: Why did the system select {curr['final_node']} as the final state?"
        )
