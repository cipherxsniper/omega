from omega_v27_registry import NodeRegistry
from omega_v27_bus import MessageBus
from omega_v27_agent import Agent
import time

class OmegaV27:

    def __init__(self):

        self.registry = NodeRegistry()
        self.bus = MessageBus()

        # create live nodes
        self.nodes = {
            "zeus": Agent("zeus", self.registry, self.bus),
            "athena": Agent("athena", self.registry, self.bus),
            "thor": Agent("thor", self.registry, self.bus)
        }

    def tick(self, input_text):

        # heartbeat all nodes
        for n in self.nodes.values():
            n.heartbeat()

        # process messages
        outputs = {}

        for name, node in self.nodes.items():

            outputs[name] = node.think(input_text)

        # cleanup dead nodes
        self.registry.cleanup()

        return {
            "active_nodes": self.registry.active_nodes(),
            "messages": self.bus.messages[-5:],
            "outputs": outputs
        }
