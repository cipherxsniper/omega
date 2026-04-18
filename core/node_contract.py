from omega.core.event_bus import emit
from omega.core.global_memory import write

class CognitiveNode:
    """
    ALL Omega nodes must inherit this contract
    """

    def process(self, event):
        result = self.compute(event)

        emit({
            "from": self.__class__.__name__,
            "type": "cognitive_signal",
            "payload": result
        })

        write({
            "from": self.__class__.__name__,
            "payload": result
        })

        return result

    def compute(self, event):
        raise NotImplementedError
