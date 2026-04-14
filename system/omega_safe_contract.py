def safe_agents(obj, fallback):
    try:
        if isinstance(obj, dict) and "agents" in obj:
            return obj["agents"]
    except:
        pass
    return fallback
