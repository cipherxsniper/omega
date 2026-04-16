def get_execution_layer():
    import importlib

    module = importlib.import_module("omega_execution_layer_v73")

    # auto-discover first valid class
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and "Execution" in name:
            return obj

    raise Exception("No execution layer found")
