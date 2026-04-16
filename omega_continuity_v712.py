# === Ω v7.12 CONTINUITY ENGINE ===

class OmegaContinuityV712:

    def __init__(self):
        self.last_event_signature = None
        self.last_state_signature = None
        self.silence_counter = 0

    def _signature(self, obj):
        try:
            if obj is None:
                return "none"
            if isinstance(obj, dict):
                return tuple(sorted(obj.items()))
            if isinstance(obj, list):
                return tuple(obj[-5:])  # last slice only
            return str(obj)
        except:
            return "unhashable"

    def should_emit(self, event, state):

        event_sig = self._signature(event)
        state_sig = self._signature(state)

        # detect repetition
        if event_sig == self.last_event_signature and state_sig == self.last_state_signature:
            self.silence_counter += 1
            return False, {
                "mode": "repetition_suppressed",
                "silence_count": self.silence_counter
            }

        # update memory
        self.last_event_signature = event_sig
        self.last_state_signature = state_sig
        self.silence_counter = 0

        return True, {
            "mode": "new_state",
            "silence_count": 0
        }

    def compress_state(self, state):
        if not isinstance(state, dict):
            return {"raw": str(state)}

        # lightweight compression: keep only signal fields
        keys = ["node", "event_type", "severity", "tick"]
        return {k: state.get(k) for k in keys if k in state}
