import os
import ast
from collections import defaultdict

class ASTBrain:

    def __init__(self, root):
        self.root = root
        self.graph = defaultdict(set)
        self.files = []

    def scan(self):
        for dirpath, _, filenames in os.walk(self.root):
            for f in filenames:
                if f.endswith(".py"):
                    self.files.append(os.path.join(dirpath, f))

    def parse_imports(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

            imports = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.add(n.name.split(".")[0])

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])

            return imports

        except Exception as e:
            return {"ERROR": str(e)}

    def build_graph(self):
        for file in self.files:
            module = os.path.basename(file).replace(".py", "")
            deps = self.parse_imports(file)

            if isinstance(deps, set):
                for d in deps:
                    self.graph[module].add(d)

    def detect_cycles(self):
        visited = set()
        stack = set()
        cycles = []

        def dfs(node):
            if node in stack:
                cycles.append(node)
                return
            if node in visited:
                return

            visited.add(node)
            stack.add(node)

            for neigh in self.graph.get(node, []):
                dfs(neigh)

            stack.remove(node)

        for node in self.graph:
            dfs(node)

        return cycles

    def report(self):
        print("\n🧠 OMEGA AST BRAIN v5 REPORT")

        print(f"\nFILES: {len(self.files)}")
        print(f"NODES: {len(self.graph)}")

        cycles = self.detect_cycles()

        print("\n⚠ CIRCULAR DEPENDENCIES:")
        for c in cycles:
            print(" -", c)

        print("\n🔗 SAMPLE GRAPH:")
        for k, v in list(self.graph.items())[:10]:
            print(f"{k} → {list(v)[:3]}")

if __name__ == "__main__":
    brain = ASTBrain("/data/data/com.termux/files/home/Omega")

    brain.scan()
    brain.build_graph()
    brain.report()
