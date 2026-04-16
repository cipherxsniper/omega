import os
import importlib.util
import inspect

OMEGA_ROOT = os.path.expanduser("~/Omega")

class OmegaNodeRegistryV71:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.health = {}
        self.meta = {}

    def register(self, name, fn):
        self.nodes[name] = fn
        self.edges.setdefault(name, {})
        self.health.setdefault(name, 1.0)

    def scan_scripts(self):
        for file in os.listdir(OMEGA_ROOT):
            if file.endswith(".py") and "omega_" in file:
                path = os.path.join(OMEGA_ROOT, file)

                try:
                    spec = importlib.util.spec_from_file_location(file[:-3], path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    for name, obj in inspect.getmembers(mod, inspect.isfunction):
                        if not name.startswith("_"):
                            node_name = f"{file[:-3]}::{name}"
                            self.register(node_name, obj)

                except Exception:
                    continue

    def node_count(self):
        return len(self.nodes)

    def connect_all(self):
        keys = list(self.nodes.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                self.edges[a][b] = self.edges[a].get(b, 0.5)
                self.edges[b][a] = self.edges[b].get(a, 0.5)

    def telemetry(self):
        return {
            "nodes": self.node_count(),
            "connections": sum(len(v) for v in self.edges.values()),
            "avg_health": sum(self.health.values()) / max(1, len(self.health))
        }
