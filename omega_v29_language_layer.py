def render(bus_event, memory_state):
    node = bus_event["node"]
    payload = bus_event["payload"]

    return f"""
🧠 Omega Node Communication

Node: {node}
Event: {bus_event['type']}

Interpretation:
The node is broadcasting a state change based on: {payload}

System Meaning:
This update propagates through the shared memory mesh, reinforcing concept evolution across the network.
"""
