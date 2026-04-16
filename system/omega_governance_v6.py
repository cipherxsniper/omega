class OmegaGovernanceV6:
    def __init__(self):
        self.required_methods = ["step"]
        self.required_keys = ["agents", "strongest", "tick"]

    def enforce(self, obj):
        # 🔧 METHOD PATCHING
        for method in self.required_methods:
            if not hasattr(obj, method):
                setattr(obj, method, self._default_step(obj))

        return obj

    def _default_step(self, obj):
        def fallback_step():
            if not hasattr(obj, "tick"):
                obj.tick = 0

            obj.tick += 1

            agents = {
                "brain_0": 0.5 + obj.tick * 0.01,
                "brain_1": 0.45 + obj.tick * 0.008,
                "brain_2": 0.4 + obj.tick * 0.007,
                "brain_3": 0.35 + obj.tick * 0.006,
            }

            return {
                "agents": agents,
                "strongest": max(agents, key=agents.get),
                "tick": obj.tick
            }

        return fallback_step

    def validate(self, rec):
        if not isinstance(rec, dict):
            return {"agents": {}, "strongest": None, "tick": 0}

        for key in self.required_keys:
            if key not in rec:
                rec[key] = {} if key == "agents" else None

        return rec
