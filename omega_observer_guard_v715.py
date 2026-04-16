class ObserverGuardV715:

    def __init__(self, observer):
        self.observer = observer

    def narrate(self, event, raw=None, field=None):

        # HARD GUARANTEE: event is valid
        if not isinstance(event, dict):
            return "[Ω OBSERVER ERROR] invalid event type"

        if "event_type" not in event:
            return "[Ω OBSERVER ERROR] missing event_type"

        try:
            return self.observer.narrate(event, raw, field)
        except Exception as e:
            return (
                "⚠️ Observer failure caught by guard layer\n"
                f"Error: {str(e)}\n"
                "System preserved stability via fallback narration."
            )
