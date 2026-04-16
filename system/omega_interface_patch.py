class OmegaInterfaceMixin:
    """
    Forces all Omega modules to be compatible with orchestrator v9+
    """

    def step(self):
        if hasattr(self, "run"):
            return self.run()
        if hasattr(self, "tick"):
            return self.tick()
        if hasattr(self, "forward"):
            return self.forward()
        raise AttributeError(f"{self.__class__.__name__} has no step-compatible method")

    def get_agents(self):
        if hasattr(self, "agents"):
            return self.agents
        if hasattr(self, "brain_states"):
            return self.brain_states
        if hasattr(self, "nodes"):
            return self.nodes
        return {}

    def normalize_output(self, data):
        if isinstance(data, dict) and "agents" not in data:
            data["agents"] = data
        return data
