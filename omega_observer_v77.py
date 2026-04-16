class OmegaObserverV77:
    def narrate(self, tick, trace, field):

        final = trace.get("final_node", "unknown")

        return (
            f"[Ω v7.7 OBSERVER]\n"
            f"Tick: {tick}\n"
            f"Final Node: {final}\n"
            f"Trace Keys: {list(trace.keys()) if isinstance(trace, dict) else type(trace)}\n"
            f"Field Snapshot: {field.get('global_memory', 'N/A')}"
        )
