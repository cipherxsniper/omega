def safe_get_agents(rec):
    if isinstance(rec, dict):
        if "agents" in rec:
            return rec["agents"]
        # fallback from brain format
        return {k: v for k, v in rec.items() if "brain" in k}
    return {}
