from pathlib import Path
import importlib
import sys

# =====================================================
# MODULE IDENTITY DATABASE
# =====================================================

MODULE_REGISTRY = {
    "swarm_bus": {
        "type": "SERVICE",
        "path": "Omega/OmegaV6/runtime_v7/core/v9_9_swarm_bus_v14.py",
        "import_as": "swarm_bus"
    },

    "memory": {
        "type": "TASK",
        "path": "Omega/omega_swarm_memory_bridge_v9.py",
        "import_as": "memory"
    },

    "assistant": {
        "type": "SERVICE",
        "path": "Omega/omega_unified_brain_v22.py",
        "import_as": "assistant"
    },

    "emitter": {
        "type": "TASK",
        "path": "Omega/OmegaV6/runtime_v7/core/test_swarm_emitter.py",
        "import_as": "emitter"
    }
}

# =====================================================
# IDENTITY RESOLVER
# =====================================================

def resolve_path(module_id: str):
    module = MODULE_REGISTRY.get(module_id)
    if not module:
        raise ValueError(f"[REGISTRY ERROR] Unknown module: {module_id}")
    return Path.home() / module["path"]

# =====================================================
# IMPORT LOADER (PATH-BASED EXECUTION)
# =====================================================

def load_module(module_id: str):
    path = resolve_path(module_id)

    if not path.exists():
        raise FileNotFoundError(f"[MISSING MODULE] {module_id} at {path}")

    spec_name = module_id + "_dynamic"

    spec = importlib.util.spec_from_file_location(spec_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec_name] = module
    spec.loader.exec_module(module)

    return module

# =====================================================
# SYSTEM BOOTSTRAP VIEW
# =====================================================

def print_registry():
    print("\n🧬 OMEGA MODULE IDENTITY REGISTRY v1\n")

    for mid, data in MODULE_REGISTRY.items():
        print("──────────────────────────────")
        print(f"MODULE ID : {mid}")
        print(f"TYPE      : {data['type']}")
        print(f"PATH      : {data['path']}")
        print(f"IMPORT AS : {data['import_as']}")

# =====================================================
# SELF-VALIDATION
# =====================================================

def validate_registry():
    print("\n🛡️ VALIDATING MODULE PATHS...\n")

    for mid, data in MODULE_REGISTRY.items():
        path = Path.home() / data["path"]

        if path.exists():
            print(f"🟢 {mid} OK")
        else:
            print(f"🔴 {mid} MISSING → {path}")

# =====================================================
# ENTRY
# =====================================================

if __name__ == "__main__":
    print_registry()
    validate_registry()
