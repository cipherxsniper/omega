from node_attention import AttentionNode
from node_goal import GoalNode
from node_memory import MemoryNode
from node_stability import StabilityNode

# SINGLE SOURCE OF NODE REALITY
NODES = {
    "attention": AttentionNode(),
    "goal": GoalNode(),
    "memory": MemoryNode(),
    "stability": StabilityNode()
}

def get_node(name):
    return NODES.get(name)
