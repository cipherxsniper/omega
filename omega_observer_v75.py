class OmegaObserverV75:
    def narrate(self, tick, trace, memory):
        try:
            gm = memory.global_memory
        except Exception:
            gm = {}

        nodes = gm.get("nodes", {}) if isinstance(gm, dict) else {}

        if trace:
            dominant = trace[-1]["node"]
        else:
            dominant = "unknown"

        health = 0
        if dominant in nodes:
            health = nodes[dominant].get("avg_health", 0)

        return (
            f"[Ω v7.5 | TICK {tick}]\n"
            f"Final node: {dominant}\n"
            f"System stability: {health:.2f}\n"
            f"Trace length: {len(trace)}\n"
        )
