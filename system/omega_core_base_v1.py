import time

class OmegaCoreBaseV1:
    """
    UNIFIED KERNEL BASE CONTRACT
    """

    def step(self) -> dict:
        raise NotImplementedError("step() MUST be implemented")

    def emit(self, agents: dict) -> dict:
        strongest = max(agents, key=agents.get)

        return {
            "agents": agents,
            "strongest": strongest,
            "status": "active",
            "timestamp": time.time()
        }

    def safe_step(self):
        """
        NEVER CRASH WRAPPER
        """
        try:
            result = self.step()

            if not isinstance(result, dict):
                return self.emit({
                    "brain_0": 0,
                    "brain_1": 0,
                    "brain_2": 0,
                    "brain_3": 0
                })

            if "agents" not in result:
                result["agents"] = {
                    "brain_0": 0,
                    "brain_1": 0,
                    "brain_2": 0,
                    "brain_3": 0
                }

            return self.emit(result["agents"])

        except Exception:
            return self.emit({
                "brain_0": 0,
                "brain_1": 0,
                "brain_2": 0,
                "brain_3": 0
            })
