import os
import ast

OMEGA_ROOT = os.path.expanduser("~/Omega")

class OmegaNodeRegistryV71Safe:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def scan_scripts(self):
        for file in os.listdir(OMEGA_ROOT):
            if file.endswith(".py") and "omega_" in file:
                path = os.path.join(OMEGA_ROOT, file)

                with open(path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                    except:
                        continue

                functions = [
                    n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                ]

                if functions:
                    self.nodes[file[:-3]] = {
                        "functions": functions,
                        "type": "static_node"
                    }

    def node_count(self):
        return len(self.nodes)

    def connect_all(self):
        keys = list(self.nodes.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                self.edges.setdefault(a, {})[b] = 0.5
                self.edges.setdefault(b, {})[a] = 0.5

    def telemetry(self):
        return {
            "nodes": self.node_count(),
            "connections": sum(len(v) for v in self.edges.values())
        }
