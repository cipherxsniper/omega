import os
import importlib.util

NODE_CACHE = {}

class FileNodeScannerV10:
    """
    Continuously scans Omega directory for new nodes.
    Auto-registers them into the bus mesh.
    """

    def scan(self, root="~/Omega"):
        root = os.path.expanduser(root)

        discovered = []

        for path, _, files in os.walk(root):
            for f in files:
                if f.endswith(".py") and "node" in f.lower():
                    full = os.path.join(path, f)
                    discovered.append(full)

        return discovered

    def load_as_node(self, file_path):
        module_name = file_path.replace("/", "_").replace(".py", "")

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        NODE_CACHE[module_name] = module
        return module
