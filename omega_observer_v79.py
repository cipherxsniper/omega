class OmegaObserverV79:

    def narrate(self, event, prev=None):

        if event["event_type"] == "route_error":
            return (
                "⚠️ Omega routing failure detected.\n"
                "Execution layer failed during node traversal.\n"
                f"Raw system output: {event['raw']}\n"
                "Interpretation: graph contract violation or missing node reference.\n"
            )

        if event["event_type"] == "success":
            return (
                "🧠 Omega execution completed successfully.\n"
                "Cognitive traversal returned a valid trace packet.\n"
                "System state remains stable under current load.\n"
            )

        return "Ω event processed with no interpretation layer."
