import os
import ast
import json
import sys
from collections import defaultdict

ROOT = "/data/data/com.termux/files/home/Omega"
REGISTRY_FILE = "omega_node_registry_v63.json"

# detect stdlib modules
STDLIB = set(sys.builtin_module_names)

class NodeClassifierV63:

    def __init__(self):
        self.files = []
        self.graph = defaultdict(set)
        self.reverse = defaultdict(set)
        self.local_modules = set()
        self.registry = {}

    def scan(self):
        for r, _, fns in os.walk(ROOT):
            for f in fns:
                if f.endswith(".py"):
                    path = os.path.join(r, f)
                    self.files.append(path)
                    name = os.path.basename(path).replace(".py", "")
                    self.local_modules.add(name)

    def parse_imports(self, file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            imports = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.add(n.name.split(".")[0])

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])

            return imports
        except:
            return set()

    def classify(self, module):
        # CORE = your Omega system naming pattern
        if module.startswith("omega") or module.startswith("node") or module.startswith("Brain"):
            return "CORE"

        # stdlib
        if module in STDLIB:
            return "STDLIB"

        # everything else = external/vendor
        return "EXTERNAL"

    def build_graph(self):
        for file in self.files:
            name = os.path.basename(file).replace(".py", "")
            deps = self.parse_imports(file)

            for d in deps:
                if d in self.local_modules:
                    self.graph[name].add(d)
                    self.reverse[d].add(name)

    def build_registry(self):
        for node in self.local_modules:
            node_type = self.classify(node)

            self.registry[node] = {
                "type": node_type,
                "depends_on": list(self.graph.get(node, [])),
                "used_by": list(self.reverse.get(node, [])),
                "connections": len(self.graph.get(node, [])) + len(self.reverse.get(node, [])),
            }

    def save(self):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self.registry, f, indent=2)

    def display(self):
        print("\n🧠 OMEGA NODE REGISTRY v6.3 (CLASSIFIED)\n")

        core_nodes = {k: v for k, v in self.registry.items() if v["type"] == "CORE"}

        ranked = sorted(core_nodes.items(), key=lambda x: x[1]["connections"], reverse=True)

        print(f"CORE NODES: {len(core_nodes)}\n")

        print("🔥 TOP CORE SYSTEM NODES:\n")
        for name, data in ranked[:10]:
            print(f"{name}")
            print(f"  connections: {data['connections']}")
            print(f"  depends_on: {data['depends_on'][:5]}")
            print(f"  used_by: {data['used_by'][:5]}")
            print("")

        print("\n⚙️ EXTERNAL NOISE (IGNORED IN RANKING):")
        for name, data in list(self.registry.items())[:10]:
            if data["type"] != "CORE":
                print(f"{name} ({data['type']})")

    def run(self):
        self.scan()
        self.build_graph()
        self.build_registry()
        self.save()
        self.display()


if __name__ == "__main__":
    NodeClassifierV63().run()
