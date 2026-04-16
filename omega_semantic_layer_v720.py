class OmegaSemanticLayerV720:

    def interpret(self, raw_state):

        node_count = len(raw_state.get("nodes", {}))
        error_rate = raw_state.get("error_rate", 0.0)
        stability = raw_state.get("stability", 0.5)

        meaning = []

        if error_rate > 0.6:
            meaning.append("System is experiencing high execution instability.")

        if node_count > 5:
            meaning.append("Multiple active cognitive nodes are interacting.")

        if stability > 0.8:
            meaning.append("System operating in highly stable regime.")

        if stability < 0.4:
            meaning.append("System stability degraded; corrective adaptation active.")

        return {
            "summary": " | ".join(meaning) if meaning else "System stable baseline operation.",
            "structured": {
                "nodes": node_count,
                "stability": stability,
                "error_rate": error_rate
            }
        }
