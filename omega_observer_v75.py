from omega_schema_v76 import normalize_trace

class OmegaObserverV75:
    def narrate(self, tick, trace, field):

        trace = normalize_trace(trace)

        dominant = trace.final_node

        stability = getattr(field.global_memory, "health", 0.5) \
            if hasattr(field, "global_memory") else 0.5

        return (
            f"System stability: {stability:.2f}\n"
            f"Trace length: {trace.steps}\n"
            f"Path: {' -> '.join(trace.path)}\n"
            f"Dominant node: {dominant}"
        )
