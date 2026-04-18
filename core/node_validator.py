from omega.core.event_bus import emit
from omega.core.global_memory import write

class NodeValidator:
    """
    Enforces cognitive integrity:
    - MUST emit
    - MUST write
    - blocks silent nodes
    """

    def validate(self, node_name, result):
        if result is None:
            raise Exception(f"[OMEGA BLOCK] {node_name} produced empty output")

        event = {
            "from": node_name,
            "type": "cognitive_signal",
            "payload": result
        }

        emit(event)
        write(event)

        return result
