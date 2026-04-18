# 🧠 Omega v11.5 Cross-Node Flow Engine

from omega_core.omega_event_bus_v11_5 import EventBus
from omega_core.omega_node_interface_v11_5 import OmegaNode

class CrossNodeEngine:

    def __init__(self):

        self.bus = EventBus()

        self.nodes = {
            "memory": OmegaNode("node_memory", self.bus),
            "goal": OmegaNode("node_goal", self.bus),
            "attention": OmegaNode("node_attention", self.bus),
            "stability": OmegaNode("node_stability", self.bus)
        }

    def run_cycle(self):

        # all nodes act
        for node in self.nodes.values():
            node.step()

        # cross injection cycle (feedback loop)
        self.bus.publish(
            "memory_update",
            "system",
            {"cycle": "sync"}
        )

        return self.bus.get_recent()
