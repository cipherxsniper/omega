from node_attention import AttentionNode
from node_goal import GoalNode
from node_memory import MemoryNode
from node_stability import StabilityNode

from omega.core.node_watchdog import NodeWatchdog

WATCHDOG = NodeWatchdog()

_raw_nodes = {
    "attention": AttentionNode(),
    "goal": GoalNode(),
    "memory": MemoryNode(),
    "stability": StabilityNode()
}

NODES = {
    name: WATCHDOG.wrap(name, node, f"core/{name}.py")
    for name, node in _raw_nodes.items()
}

def get_node(name):
    return NODES.get(name)
