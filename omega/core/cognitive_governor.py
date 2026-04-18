import time
from omega.core.node_registry import registry
from omega.core.node_enforcer import EnforcedNode
from omega.core.node_self_repair import repair_engine
from omega.core.global_memory import write

class CognitiveGovernor:
    """
    Continuously enforces system integrity in real time.
    """

    def __init__(self):
        self.enforced_nodes = {}

    def initialize(self):
        for name, node in registry.all().items():
            repaired = repair_engine.repair(node)
            self.enforced_nodes[name] = EnforcedNode(repaired)

    def tick(self, event):
        for name, node in self.enforced_nodes.items():
            node.process(event)

    def run_forever(self):
        self.initialize()

        while True:
            event = {"type": "heartbeat", "timestamp": time.time()}

            write({
                "type": "governor_tick",
                "event": event
            })

            self.tick(event)
            time.sleep(0.5)

governor = CognitiveGovernor()
