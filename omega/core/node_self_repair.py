import inspect
from omega.core.global_memory import write

class NodeSelfRepair:
    """
    Detects broken nodes and patches missing emit/write behavior.
    """

    def repair(self, node):
        source = inspect.getsource(node.__class__)

        if "emit(" not in source or "write(" not in source:
            write({
                "type": "self_repair_trigger",
                "node": node.__class__.__name__
            })

            # SAFE PATCH INJECTION (non-destructive)
            node._force_repair_mode = True

            def patched_compute(event):
                result = node.compute(event)

                # forced compliance layer
                from omega.core.event_bus import emit
                from omega.core.global_memory import write

                emit({
                    "from": node.__class__.__name__,
                    "type": "repair_emission",
                    "payload": result
                })

                write({
                    "node": node.__class__.__name__,
                    "result": result,
                    "repair": True
                })

                return result

            node.compute = patched_compute

        return node

repair_engine = NodeSelfRepair()
