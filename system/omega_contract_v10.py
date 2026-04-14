class OmegaContractV10:
    """
    HARD SYSTEM CONTRACT:
    Every engine must output this format:
    {
        agents: dict[str, float],
        strongest: str,
        metrics: dict,
        status: str
    }
    """

    @staticmethod
    def normalize(output):
        if not isinstance(output, dict):
            output = {}

        agents = output.get("agents") or output.get("scores") or {}

        if isinstance(agents, list):
            agents = {f"brain_{i}": float(v) for i, v in enumerate(agents)}

        if not isinstance(agents, dict):
            agents = {"brain_0": 1.0}

        strongest = output.get("strongest")
        if not strongest:
            strongest = max(agents, key=agents.get)

        return {
            "agents": agents,
            "strongest": strongest,
            "metrics": output.get("metrics", {}),
            "status": output.get("status", "active")
        }
