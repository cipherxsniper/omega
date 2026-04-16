class OmegaContractV714:

    REQUIRED_EVENT_KEYS = {
        "event_type",
        "node",
        "tick",
        "raw"
    }

    @staticmethod
    def normalize(tick, node, raw):
        return {
            "event_type": "state_update",
            "node": node,
            "tick": tick,
            "raw": raw
        }

    @staticmethod
    def validate(event):
        if not isinstance(event, dict):
            return False, "event not dict"

        missing = [k for k in OmegaContractV714.REQUIRED_EVENT_KEYS if k not in event]

        if missing:
            return False, f"missing keys: {missing}"

        return True, None
