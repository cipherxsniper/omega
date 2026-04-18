"""
OMEGA COGNITIVE BUS NODE CONTRACT
Every node in the system must follow this execution protocol.
"""

from omega.core.event_bus import emit
from omega.core.global_memory import write

class CognitiveNode:
    """
    Base class that enforces Omega cognition flow:
    Node → Compute → Emit → Memory Write → Bus Propagation
    """

    def compute(self, event):
        """
        Override this in all child nodes.
        """
        raise NotImplementedError("compute() must be implemented by node")

    def process(self, event):
        result = self.compute(event)

        # 1. Emit into global cognitive bus
        emit({
            "from": self.__class__.__name__,
            "type": "cognitive_signal",
            "payload": result
        })

        # 2. Persist into global memory field
        write({
            "node": self.__class__.__name__,
            "result": result,
            "input": event
        })

        return result
