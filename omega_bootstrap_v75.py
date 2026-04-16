import importlib

def get_execution_layer():

    # Try known module versions in order
    candidates = [
        ("omega_execution_layer_v73", "OmegaExecutionLayerV73"),
        ("omega_execution_layer_v70", "OmegaExecutionLayerV70"),
        ("omega_execution_layer_v68", "OmegaExecutionLayerV68"),
    ]

    for module_name, class_name in candidates:
        try:
            mod = importlib.import_module(module_name)
            cls = getattr(mod, class_name)
            return cls
        except Exception:
            continue

    # LAST RESORT: try any execution layer class in system
    import sys, inspect

    for mod_name, mod in sys.modules.items():
        if not mod:
            continue
        for name, obj in inspect.getmembers(mod):
            if "ExecutionLayer" in name:
                return obj

    raise Exception("No execution layer found")
