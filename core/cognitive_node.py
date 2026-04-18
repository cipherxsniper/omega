from omega.core.event_bus import emit
from omega.core.global_memory import write
import numpy as np

class CognitiveNode:
    def __init__(self, node_id):
        self.id = node_id
        self.state = {}

    def compute(self, event):
        return {
            "processed_by": self.id,
            "variance": np.random.random(),
            "signal_strength": np.random.random(),
            "payload": event
        }

    def process(self, event):
        result = self.compute(event)

        emit({
            "from": self.id,
            "type": "cognitive_signal",
            "payload": result
        })

        write({
            "node": self.id,
            "data": result
        })

        return result
