import os
import ast
from datetime import datetime

REGISTRY_PATH = "/data/data/com.termux/files/home/Omega/omega_registry_v43.log"

# ================================
# FUNCTION REGISTRY CORE
# ================================

def scan_file_functions(file_path):
    """Extract all function names from a Python file."""
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read(), filename=file_path)

        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

        return functions
    except Exception as e:
        return [f"ERROR: {e}"]


def register_system_state(base_path="/data/data/com.termux/files/home/Omega"):
    """Scan entire system and log function map."""
    registry = {}

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                registry[path] = scan_file_functions(path)

    with open(REGISTRY_PATH, "w") as log:
        log.write(f"Ω REGISTRY SNAPSHOT {datetime.now()}\n\n")
        for k, v in registry.items():
            log.write(f"{k}\n")
            log.write(f"  {v}\n\n")

    return registry


def check_function_exists(function_name, registry):
    """Check if function exists anywhere in system."""
    for file, funcs in registry.items():
        if function_name in funcs:
            return True
    return False


def validate_patch(old_name, new_name, registry):
    """
    Prevent unsafe renames.
    """
    old_exists = check_function_exists(old_name, registry)
    new_exists = check_function_exists(new_name, registry)

    if old_exists and not new_exists:
        print(f"[Ω REGISTRY WARNING] Unsafe rename detected:")
        print(f"  {old_name} → {new_name}")
        return False

    return True


def log_event(event):
    with open(REGISTRY_PATH, "a") as log:
        log.write(f"[EVENT] {datetime.now()} | {event}\n")
