# PATCH LOADER

import importlib.util
import glob

def load_patch(path):
    spec = importlib.util.spec_from_file_location("patch", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def apply_all(core):
    for patch_file in glob.glob("patch_*.py"):
        patch = load_patch(patch_file)

        if hasattr(patch, "apply_patch"):
            core = patch.apply_patch(core)

    return core
