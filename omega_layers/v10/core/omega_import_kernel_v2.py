import ast
from pathlib import Path

MODULE_REGISTRY = {
    "omega_consensus_engine_v10": "omega_layers.v10.core.omega_consensus_engine_v10",
    "omega_consensus_runtime_v10": "omega_layers.v10.runtime.omega_consensus_runtime_v10",
    "omega_auto_import_repair_v10": "omega_layers.v10.policies.omega_auto_import_repair_v10",
}

class ImportResolutionKernel:

    def __init__(self, registry):
        self.registry = registry

    def resolve(self, code: str):
        tree = ast.parse(code)
        lines = code.splitlines()
        updated = lines[:]

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    if node.module in self.registry:
                        new_module = self.registry[node.module]
                        updated[node.lineno - 1] = updated[node.lineno - 1].replace(
                            node.module,
                            new_module
                        )

        return "\n".join(updated)


def validate_registry(registry):
    reverse = {}
    for k, v in registry.items():
        if v in reverse:
            raise Exception(f"COLLISION: {v}")
        reverse[v] = k
    return True


def repair_file(path):
    kernel = ImportResolutionKernel(MODULE_REGISTRY)

    code = Path(path).read_text()

    for _ in range(3):
        new_code = kernel.resolve(code)
        if new_code == code:
            break
        code = new_code

    Path(path).write_text(code)
    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: python omega_import_kernel_v2.py <file>")
        exit()

    validate_registry(MODULE_REGISTRY)
    repair_file(sys.argv[1])
    print("🧠 IMPORT RESOLUTION COMPLETE (v2)")
