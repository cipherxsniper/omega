class OmegaObserverV75:
    def narrate(self, tick, trace, memory):
        lines = []
        lines.append(f"Tick {tick} analysis:")

        for step in trace:
            node = step["node"]
            health = step["result"].get("health", 0)

            lines.append(
                f"- Node '{node}' executed with health {health:.2f}"
            )

        dominant = max(trace, key=lambda x: x["result"].get("health", 0))["node"]

        lines.append(f"Dominant node this tick: {dominant}")
        lines.append(
            f"System stability: {memory['global_memory']['nodes'].get(dominant, {}).get('avg_health', 0):.2f}"
        )

        return "\n".join(lines)
