from omega_v30_node_factory import spawn_node
from omega_v30_self_modify import propose_change
from omega_v30_execution_graph import execute_node

def generate_reply(intent, message, history):
    if "spawn" in message.lower():
        name = message.split()[-1]
        return spawn_node(name)

    if "modify" in message.lower():
        return propose_change("app_brain", "logic_update", message)

    return execute_node("app_brain", message)
