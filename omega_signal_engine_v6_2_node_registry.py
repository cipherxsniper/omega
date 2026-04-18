import os
import ast
import json
from collections import defaultdict

ROOT = "/data/data/com.termux/files/home/Omega"
REGISTRY_FILE = "omega_node_registry.json"

class NodeRegistryV62:

    def __init__(self):
        self.files = []
        self.graph = defaultdict(set)
        self.reverse = defaultdict(set)
        self.local_modules = set()
        self.registry = {}

    # -------------------------
    # SCAN FILES
    # -------------------------
    def scan(self):
        for r, _, fns in os.walk(ROOT):
            for f in fns:
                if f.endswith(".py"):
                    path = os.path.join(r, f)
                    self.files.append(path)

                    name = os.path.basename(path).replace(".py", "")
                    self.local_modules.add(name)

    # -------------------------
    # PARSE IMPORTS
    # -------------------------
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

    # -------------------------
    # BUILD GRAPH (FILTERED)
    # -------------------------
    def build_graph(self):
        for file in self.files:
            name = os.path.basename(file).replace(".py", "")
            deps = self.parse_imports(file)

            for d in deps:
                if d in self.local_modules:
                    self.graph[name].add(d)
                    self.reverse[d].add(name)

    # -------------------------
    # BUILD NODE REGISTRY
    # -------------------------
    def build_registry(self):
        for node in self.local_modules:
            self.registry[node] = {
                "depends_on": list(self.graph.get(node, [])),
                "used_by": list(self.reverse.get(node, [])),
                "connections": len(self.graph.get(node, [])) + len(self.reverse.get(node, [])),
                "status": "active" if node in self.graph else "idle"
            }

    # -------------------------
    # SAVE MEMORY
    # -------------------------
    def save_registry(self):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self.registry, f, indent=2)

    # -------------------------
    # LOAD MEMORY
    # -------------------------
    def load_registry(self):
        if os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "r") as f:
                self.registry = json.load(f)

    # -------------------------
    # DISPLAY SYSTEM
    # -------------------------
    def display(self):
        print("\n🧠 OMEGA NODE REGISTRY v6.2\n")

        print(f"TOTAL NODES: {len(self.registry)}\n")

        # Top connected nodes (real system cores)
        ranked = sorted(self.registry.items(), key=lambda x: x[1]["connections"], reverse=True)

        print("🔥 TOP CONNECTED NODES:\n")
        for name, data in ranked[:10]:
            print(f"{name}")
            print(f"  connections: {data['connections']}")
            print(f"  depends_on: {data['depends_on'][:5]}")
            print(f"  used_by: {data['used_by'][:5]}")
            print("")

        # Show active network sample
        print("\n🔗 ACTIVE CONNECTION MAP (sample):\n")
        count = 0
        for node, deps in self.graph.items():
            for d in deps:
                print(f"{node} → {d}")
                count += 1
                if count > 30:
                    return

    # -------------------------
    # TRACE NODE CONNECTIONS
    # -------------------------
    def trace_node(self, node):
        print(f"\n🧠 NODE TRACE: {node}\n")

        if node not in self.registry:
            print("Node not found.")
            return

        data = self.registry[node]

        print("DEPENDS ON:")
        for d in data["depends_on"]:
            print(f"  → {d}")

        print("\nUSED BY:")
        for u in data["used_by"]:
            print(f"  → {u}")

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        self.scan()
        self.build_graph()
        self.build_registry()
        self.save_registry()
        self.display()

        # example trace
        self.trace_node("omega_bus")


if __name__ == "__main__":
    engine = NodeRegistryV62()
    engine.run()
