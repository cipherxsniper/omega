class OmegaGovernanceV7:
    """
    Self-healing governance layer:
    - Normalizes agent schemas
    - Forces .step() compatibility
    - Repairs missing keys like 'agents'
    """

    def __init__(self):
        self.failures = 0
        self.last_valid_state = {}

    def normalize_output(self, rec):
        """
        Forces all recursive engines into a standard format:
        {
            "agents": {...},
            "metrics": {...},
            "meta": {...}
        }
        """

        if rec is None:
            return self.last_valid_state

        # FIX: missing agents
        if "agents" not in rec:
            rec["agents"] = rec.get("scores", rec.get("nodes", {}))

        # FIX: ensure numeric map
        if isinstance(rec.get("agents"), list):
            rec["agents"] = {f"agent_{i}": v for i, v in enumerate(rec["agents"])}

        # FIX: metrics fallback
        rec.setdefault("metrics", {})
        rec.setdefault("meta", {})

        self.last_valid_state = rec
        return rec

    def safe_step(self, engine):
        """
        Wraps any engine and guarantees .step() exists
        """

        if not hasattr(engine, "step"):
            def fallback_step():
                return {
                    "agents": getattr(engine, "agents", {"brain_0": 1.0}),
                    "metrics": {"fallback": True},
                    "meta": {"patched": "governance_v7"}
                }
            engine.step = fallback_step

        return engine.step()
