def swarm_snapshot(registry):
    return {
        "total_nodes": len(registry["nodes"]),
        "active_brains": [
            n for n in registry["nodes"]
            if "brain" in n["file"]
        ],
        "system_health": "stable",
        "emergence_level": 0.62
    }


def build_response(msg, registry):
    response = {
        "input": msg,
        "swarm_state": swarm_snapshot(registry),
        "analysis": "distributed cognition simulated across omega mesh",
    }
    return response

# ===== NEXUS v9 SWARM UPGRADE =====

def swarm_snapshot(registry):
    return {
        "total_nodes": len(registry["nodes"]),
        "active_brains": [
            n for n in registry["nodes"]
            if "brain" in n["file"]
        ],
        "system_health": "stable",
        "emergence_level": 0.62
    }


def build_response(msg, registry):
    response = {
        "input": msg,
        "swarm_state": swarm_snapshot(registry),
        "analysis": "distributed cognition simulated across omega mesh",
    }
    return response

# ===== END PATCH =====
