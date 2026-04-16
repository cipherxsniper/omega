import importlib

def safe_import(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError:
        print(f"[IMPORT GUARD] Missing: {name}")
        return None
