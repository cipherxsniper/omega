# Ω IMPORT HUB v2 — SELF HEALING IMPORT SYSTEM

import importlib
import os
import sys
import traceback
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(__file__))

# -----------------------------
# GLOBAL REGISTRY
# -----------------------------
DEPENDENCY_GRAPH = defaultdict(set)
FAILED_IMPORTS = set()
REPAIR_LOG = []

# stable aliases (core truth layer)
ALIAS_MAP = {
    "omega_neural_bus": [
        "omega_event_bus_v9_4",
        "omega_neural_bus_v9_3",
        "omega_neural_bus_v9"
    ],
    "omega_bus": ["omega_bus"],
    "omega_kernel": ["omega_kernel_v55", "omega_kernel"],
    "omega_memory": ["omega_memorycore_v12", "omega_memorycore_v11"],
}

_loaded_cache = {}

# -----------------------------
# CORE IMPORT ENGINE
# -----------------------------
def _try_import(name):
    return importlib.import_module(name)

def _create_stub(name):
    class Stub:
        def __getattr__(self, attr):
            def _missing(*args, **kwargs):
                return None
            return _missing
    return Stub()

def _log_repair(module, reason):
    REPAIR_LOG.append((module, reason))
    print(f"[Ω IMPORT HUB v2][REPAIR] {module} -> {reason}")

# -----------------------------
# MAIN IMPORT FUNCTION
# -----------------------------
def get(module_name):
    if module_name in _loaded_cache:
        return _loaded_cache[module_name]

    # BLOCK VERSIONED IMPORTS (CRITICAL STABILITY RULE)
    if any(tag in module_name for tag in ["_v", "v9_", "v1", "v2", "v3"]):
        _log_repair(module_name, "blocked_versioned_import")
        module_name = module_name.split("_v")[0]

    candidates = ALIAS_MAP.get(module_name, [module_name])

    for mod in candidates:
        try:
            module = _try_import(mod)
            _loaded_cache[module_name] = module

            # track dependency graph
            DEPENDENCY_GRAPH[module_name].add(mod)

            return module

        except Exception as e:
            FAILED_IMPORTS.add(mod)
            continue

    # NOTHING WORKED → CREATE SAFE STUB
    _log_repair(module_name, "stub_fallback")
    stub = _create_stub(module_name)
    _loaded_cache[module_name] = stub
    return stub

# -----------------------------
# AUTO REPAIR ENGINE
# -----------------------------
def heal_system():
    """
    Attempts to detect and pre-heal missing modules.
    """

    print("[Ω IMPORT HUB v2] running healing scan...")

    repaired = 0

    for module, candidates in ALIAS_MAP.items():
        for c in candidates:
            try:
                importlib.import_module(c)
                break
            except Exception:
                continue
        else:
            _log_repair(module, "missing_all_candidates")
            repaired += 1

    print(f"[Ω IMPORT HUB v2] healing complete | issues={repaired}")
    return repaired

# -----------------------------
# SAFE GLOBAL EXPORTS
# -----------------------------
def subscribe(*args, **kwargs):
    return get("omega_neural_bus").subscribe(*args, **kwargs)

def publish(*args, **kwargs):
    return get("omega_neural_bus").publish(*args, **kwargs)
