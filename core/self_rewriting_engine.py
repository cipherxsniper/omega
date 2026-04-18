import os
import traceback
from datetime import datetime

class SelfRewritingEngine:
    """
    Detects broken nodes, isolates them, and applies safe patches.
    """

    def __init__(self, node_registry_path="core/node_registry.py"):
        self.node_registry_path = node_registry_path
        self.failure_log = []

    def capture_failure(self, node_name, error):
        entry = {
            "node": node_name,
            "error": str(error),
            "trace": traceback.format_exc(),
            "time": datetime.utcnow().isoformat()
        }
        self.failure_log.append(entry)
        return entry

    def analyze_failure(self, failure):
        """
        Simple heuristic classifier:
        - import error → missing dependency patch
        - attribute error → broken interface
        - emit failure → contract violation
        """
        err = failure["error"].lower()

        if "import" in err:
            return "dependency_patch"
        elif "attribute" in err:
            return "interface_patch"
        elif "emit" in err:
            return "contract_patch"
        else:
            return "generic_repair"

    def generate_patch(self, node_name, failure_type):
        """
        Generates safe corrective patch code.
        """
        if failure_type == "contract_patch":
            return f"""
# AUTO-PATCH: contract enforcement fix
from omega.core.event_bus import emit
from omega.core.global_memory import write

def safe_emit(node, payload):
    event = {{
        "from": node,
        "type": "cognitive_signal",
        "payload": payload
    }}
    emit(event)
    write(event)
"""

        if failure_type == "interface_patch":
            return f"""
# AUTO-PATCH: interface correction stub
class {node_name}Fixed:
    def process(self, event):
        return event
"""

        if failure_type == "dependency_patch":
            return "# AUTO-PATCH: dependency warning - manual review required\n"

        return "# AUTO-PATCH: generic repair applied\n"

    def apply_patch(self, node_file, patch_code):
        """
        Safe append-only patching (never deletes original code)
        """
        try:
            with open(node_file, "a") as f:
                f.write("\n\n# === OMEGA SELF-REPAIR PATCH ===\n")
                f.write(patch_code)
            return True
        except Exception as e:
            return str(e)

    def repair_node(self, node_name, node_file, error):
        failure = self.capture_failure(node_name, error)
        repair_type = self.analyze_failure(failure)
        patch = self.generate_patch(node_name, repair_type)
        return self.apply_patch(node_file, patch)
