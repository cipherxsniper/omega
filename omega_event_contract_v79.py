class OmegaEventContractV79:

    @staticmethod
    def build(event_type, source, raw=None, system_state=None, severity=0.0):

        return {
            "event_type": event_type,
            "source": source,
            "raw": raw,
            "system_state": system_state or {},
            "severity": float(severity),
            "interpretation": ""
        }

    @staticmethod
    def validate(event):
        required = ["event_type", "source", "raw", "system_state", "severity", "interpretation"]
        for k in required:
            if k not in event:
                raise Exception(f"[OMEGA CONTRACT ERROR] Missing field: {k}")
        return True
