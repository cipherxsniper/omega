import json
import time

def translate_registry(registry):
    lines = []
    nodes = registry.get("nodes", {})

    lines.append("🧠 OMEGA OBSERVER REPORT")
    lines.append("------------------------")

    for node_id, data in nodes.items():
        status = data.get("status", "unknown")
        load = data.get("load", 0)
        last = data.get("last_seen", 0)

        age = round(time.time() - last, 2)

        lines.append(
            f"Node '{node_id}' is {status}, "
            f"system load at {load:.2f}, "
            f"last seen {age}s ago."
        )

    lines.append("------------------------")
    lines.append(f"Total Active Nodes: {len(nodes)}")

    return "\n".join(lines)
