import ast
import importlib.util
from pathlib import Path

ROOT = Path.home() / "Omega"

MODULE_REGISTRY = {
    "core": "omega_layers.v10.core",
    "runtime": "omega_layers.v10.runtime",
    "policies": "omega_layers.v10.policies"
}

# ----------------------------
# FIND REAL MODULE
# ----------------------------
def module_exists(module_path: str) -> bool:
    return importlib.util.find_spec(module_path) is not None


# ----------------------------
# NORMALIZE IMPORT
# ----------------------------
def normalize_import(module: str) -> str:
    parts = module.split(".")

    # collapse duplicates like omega_layers.v10.omega_layers.v10
    cleaned = []
    for p in parts:
        if not cleaned or cleaned[-1] != p:
            cleaned.append(p)

    return ".".join(cleaned)


# ----------------------------
# RESOLVE MODULE
# ----------------------------
def resolve_module(module: str) -> str:
    module = normalize_import(module)

    # direct exists
    if module_exists(module):
        return module

    # try registry mapping
    for key, base in MODULE_REGISTRY.items():
        if module.startswith(key):
            candidate = module.replace(key, base, 1)
            if module_exists(candidate):
                return candidate

    return module  # fallback (unknown but preserved)


# ----------------------------
# AST IMPORT FIXER
# ----------------------------
class ImportFixer(ast.NodeTransformer):
    def visit_ImportFrom(self, node):
        if node.module:
            node.module = resolve_module(node.module)
        return node


# ----------------------------
# ENGINE
# ----------------------------
def repair_file(path):
    path = Path(path)
    code = path.read_text()

    tree = ast.parse(code)
    tree = ImportFixer().visit(tree)

    fixed = ast.unparse(tree)

    path.write_text(fixed)
    print("🧠 IMPORT RESOLUTION COMPLETE (v3)")


# ----------------------------
# ENTRY
# ----------------------------
if __name__ == "__main__":
    import sys
    repair_file(sys.argv[1])
