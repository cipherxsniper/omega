class OmegaContinuityV712:

    def __init__(self):
        self.last_state = None

    def should_emit(self, event, state_view):
        if not event:
            return False, {"mode": "null_event"}

        if self.last_state == state_view:
            return False, {"mode": "suppressed_repeat"}

        self.last_state = state_view
        return True, {"mode": "emit_change"}

    def compress_state(self, state_view):
        return {
            "node": state_view.get("node"),
            "tick": state_view.get("tick"),
            "event": state_view.get("event_type")
        }
