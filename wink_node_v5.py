import random

def spawn_node(node_id):
    return {
        "id": node_id,
        "curiosity": random.random(),
        "focus": random.random(),
        "instability": random.random() * 0.3,
        "signal": 0.0
    }

def update_node(node):
    node["curiosity"] = max(0, min(1, node["curiosity"] + random.uniform(-0.02, 0.03)))
    node["focus"] = max(0, min(1, node["focus"] + random.uniform(-0.02, 0.03)))
    node["instability"] = max(0, min(1, node["instability"] + random.uniform(-0.01, 0.02)))

    node["signal"] = (
        node["curiosity"] * 0.4 +
        node["focus"] * 0.4 -
        node["instability"] * 0.3
    )

    return node
