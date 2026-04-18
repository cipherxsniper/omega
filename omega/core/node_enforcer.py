from omega.core.cognitive_validator import validator
from omega.core.event_bus import emit
from omega.core.global_memory import write

class EnforcedNode:
    """
    Wraps any node and guarantees:
    - emit happens
    - memory write happens
    - validation is executed
    """

    def __init__(self, node):
        self.node = node
        self.error_count = 0

    def process(self, event):
        event_emitted = False
        memory_written = False

        try:
            result = self.node.compute(event)

            # FORCE EMIT (cannot be skipped)
            emit({
                "from": self.node.__class__.__name__,
                "type": "cognitive_signal",
                "payload": result
            })
            event_emitted = True

            # FORCE MEMORY WRITE
            write({
                "node": self.node.__class__.__name__,
                "result": result,
                "input": event
            })
            memory_written = True

            return result

        except Exception as e:
            self.error_count += 1

            write({
                "type": "node_error",
                "node": self.node.__class__.__name__,
                "error": str(e)
            })

            return None

        finally:
            validator.score_node(
                self.node.__class__.__name__,
                event_emitted,
                memory_written,
                self.error_count
            )
