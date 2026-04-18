from node_scanner import scan_nodes
from agent_registry import AgentRegistry
from message_bus import MessageBus
from self_modifier import SelfModifier

class OmegaV25:

    def __init__(self):

        self.registry = AgentRegistry()
        self.bus = MessageBus()
        self.modifier = SelfModifier()

        self.load_nodes()

    def load_nodes(self):

        nodes = scan_nodes(".")

        for n in nodes:
            self.registry.register(n)

    def tick(self, input_text):

        nodes = list(self.registry.nodes.keys())

        # simple distribution of thought
        for node in nodes[:3]:

            self.bus.send("omega_core", node, input_text)

        return {
            "nodes_active": nodes[:5],
            "messages": len(self.bus.messages),
            "patches": self.modifier.list_patches()
        }
