from omega.core.event_bus import subscribe

class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def register(self, name, node):
        self.nodes[name] = node
        subscribe(node.process)

    def get(self, name):
        return self.nodes.get(name)

    def all(self):
        return self.nodes

registry = NodeRegistry()

# CORE NODES (authoritative cognition layer)
from node_attention import AttentionNode
from node_goal import GoalNode
from node_memory import MemoryNode
from node_stability import StabilityNode

registry.register("attention", AttentionNode())
registry.register("goal", GoalNode())
registry.register("memory", MemoryNode())
registry.register("stability", StabilityNode())
