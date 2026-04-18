from omega.core.self_rewriting_engine import SelfRewritingEngine
import traceback

ENGINE = SelfRewritingEngine()

class NodeWatchdog:
    """
    Observes node execution and auto-heals failures.
    """

    def wrap(self, node_name, node_obj, node_file):

        def safe_process(event):
            try:
                return node_obj.process(event)

            except Exception as e:
                print(f"[OMEGA WATCHDOG] Failure detected in {node_name}")
                ENGINE.repair_node(node_name, node_file, e)
                return {"status": "repaired", "node": node_name}

        return safe_process
