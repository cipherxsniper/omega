GLOBAL_MEMORY = {
    "packets": [],
    "transitions": [],
    "attractors": {},
    "node_states": {}
}

def write(event):
    GLOBAL_MEMORY["packets"].append(event)

def snapshot():
    return GLOBAL_MEMORY

def update_node_state(node_id, state):
    GLOBAL_MEMORY["node_states"][node_id] = state
