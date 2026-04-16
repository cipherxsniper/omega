# Ω IMPORT HUB v1
# Single source of truth for all Omega imports

import importlib
import sys
import os

BASE = os.path.dirname(os.path.dirname(__file__))

# Register known stable mappings
MODULE_MAP = {
    # BUS LAYER
    "omega_neural_bus": "omega_event_bus_v9_4",
    "neural_bus": "omega_event_bus_v9_4",

    # CORE SYSTEM
    "omega_bus": "omega_bus",
    "omega_kernel": "omega_kernel",

    # MEMORY
    "omega_memory": "omega_memorycore_v12",

    # MESH
    "omega_mesh": "omega_mesh_kernel_v7",
}

_loaded_cache = {}

def get(module_name):
    """
    Safe import wrapper for all Omega modules.
    Never import versioned modules directly again.
    """

    if module_name in _loaded_cache:
        return _loaded_cache[module_name]

    real_name = MODULE_MAP.get(module_name, module_name)

    try:
        module = importlib.import_module(real_name)
        _loaded_cache[module_name] = module
        return module

    except Exception as e:
        print(f"[Ω IMPORT HUB] FAILED: {real_name} -> {e}")

        # fallback stub so system NEVER crashes
        class Stub:
            def __getattr__(self, name):
                def _missing(*args, **kwargs):
                    return None
                return _missing

        stub = Stub()
        _loaded_cache[module_name] = stub
        return stub


def subscribe(*args, **kwargs):
    return get("omega_neural_bus").subscribe(*args, **kwargs)


def publish(*args, **kwargs):
    return get("omega_neural_bus").publish(*args, **kwargs)
