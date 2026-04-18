import os
import ast
from collections import defaultdict

class ASTBrain:

    def __init__(self, root):
        self.root = root
        self.graph = defaultdict(set)
        self.files = []
        self.local_modules = set()

    def scan(self):
        for dirpath, _, filenames in os.walk(self.root):
            for f in filenames:
                if f.endswith(".py"):
                    path = os.path.join(dirpath, f)
                    self.files.append(path)

                    name = os.path.basename(path).replace(".py", "")
                    self.local_modules.add(name)

    def parse_imports(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
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

    def build_graph(self):
        for file in self.files:
            module = os.path.basename(file).replace(".py", "")
            deps = self.parse_imports(file)

            for d in deps:
                # ✅ ONLY TRACK INTERNAL MODULES
                if d in self.local_modules:
                    self.graph[module].add(d)

    def detect_cycles(self):
        visited = set()
        stack = set()
        cycles = []

        def dfs(node, path):
            if node in path:
                cycles.append(path[path.index(node):] + [node])
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)

            for neigh in self.graph.get(node, []):
                dfs(neigh, path)

            path.pop()

        for node in self.graph:
            dfs(node, [])

        return cycles

    def report(self):
        print("\n🧠 OMEGA AST BRAIN v5 (CORRECTED)\n")

        print(f"FILES: {len(self.files)}")
        print(f"INTERNAL NODES: {len(self.graph)}")

        cycles = self.detect_cycles()

        print("\n⚠ REAL CIRCULAR DEPENDENCIES:")
        for c in cycles[:20]:
            print(" → ".join(c))

        print("\n🔗 SAMPLE GRAPH:")
        for k, v in list(self.graph.items())[:10]:
            print(f"{k} → {list(v)}")

if __name__ == "__main__":
    brain = ASTBrain("/data/data/com.termux/files/home/Omega")
    brain.scan()
    brain.build_graph()
    brain.report()
