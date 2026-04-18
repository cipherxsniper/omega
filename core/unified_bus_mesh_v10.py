import importlib
import os
from omega.core.event_bus import emit, subscribe

class UnifiedBusMeshV10:
    """
    Forces ALL nodes to communicate only via event bus.
    """

    def connect_node(self, node_name, node_obj):
        def wrapped_process(event):
            result = node_obj.process(event)

            emit({
                "from": node_name,
                "type": "mesh_signal",
                "payload": result
            })

            return result

        subscribe(node_name, wrapped_process)
        return wrapped_process

    def broadcast(self, event):
        return emit(event)
