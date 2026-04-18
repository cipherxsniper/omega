def to_english(event):
    node = event["node"]
    action = event["type"]
    cpu = event["payload"].get("cpu", 0)
    mem = event["payload"].get("memory", 0)

    return (
        f"Node {node} reported a {action} event. "
        f"CPU load is {cpu:.2f}, memory load is {mem:.2f}. "
        f"System status is being tracked for stability."
    )
