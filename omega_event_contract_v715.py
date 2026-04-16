class OmegaEventContractV715:

    REQUIRED_KEYS = {
        "tick",
        "event_type",
        "node",
        "raw",
        "state",
        "severity"
    }

    @staticmethod
    def build(tick, event_type, node, raw, state=None, severity=0.5):
        return {
            "tick": tick,
            "event_type": event_type,
            "node": node,
            "raw": raw,
            "state": state or {},
            "severity": float(severity)
        }

    @staticmethod
    def validate(event):
        if not isinstance(event, dict):
            return False, "EVENT_NOT_DICT"

        for k in OmegaEventContractV715.REQUIRED_KEYS:
            if k not in event:
                return False, f"MISSING_KEY:{k}"

        return True, None

    @staticmethod
    def safe(event):
        ok, err = OmegaEventContractV715.validate(event)

        if ok:
            return event

        return OmegaEventContractV715.build(
            tick=event.get("tick", -1),
            event_type="contract_violation",
            node=event.get("node", None),
            raw=str(err),
            state={},
            severity=1.0
        )
