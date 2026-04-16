class OmegaObserverV77:
    def narrate(self, tick, trace, model):
        dominant = trace[-1]["node"] if trace else "unknown"

        return {
            "tick": tick,
            "thought": f"Node {dominant} dominated last cycle.",
            "self_view": {
                "entropy": model.behavior["entropy_preference"],
                "coherence": model.memory["confidence"],
                "strategy": model.behavior["dominant_strategy"]
            },
            "trace_summary": [
                {"node": t["node"], "health": t["result"]["health"]}
                for t in trace
            ]
        }
