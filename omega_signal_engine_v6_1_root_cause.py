import os
import ast
from collections import defaultdict, deque

ROOT = "/data/data/com.termux/files/home/Omega"

class RootCauseTracerV61:

    def __init__(self):
        self.files = []
        self.graph = defaultdict(set)        # forward deps
        self.reverse = defaultdict(set)      # reverse deps
        self.local_modules = set()

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
    # BUILD GRAPH
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
    # ROOT CAUSE TRACE
    # -------------------------
    def trace_impact(self, root_node):
        visited = set()
        queue = deque([root_node])
        impact = []

        while queue:
            node = queue.popleft()

            for dep in self.reverse.get(node, []):
                if dep not in visited:
                    visited.add(dep)
                    impact.append(dep)
                    queue.append(dep)

        return impact

    # -------------------------
    # RANK ROOT CAUSES
    # -------------------------
    def rank_root_causes(self):
        ranking = []

        for node in self.local_modules:
            impact = self.trace_impact(node)
            score = len(impact)

            if score > 0:
                ranking.append((node, score, impact))

        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking

    # -------------------------
    # REPORT
    # -------------------------
    def report(self):
        print("\n🧠 OMEGA SIGNAL ENGINE v6.1 (ROOT CAUSE TRACER)\n")

        ranking = self.rank_root_causes()

        print("🔥 TOP ROOT CAUSES BY IMPACT:\n")

        for node, score, impact in ranking[:10]:
            print(f"ROOT NODE: {node}")
            print(f"IMPACT SIZE: {score}")

            # show first few downstream nodes
            preview = impact[:10]
            for d in preview:
                print(f"   → {d}")

            if score > 10:
                print(f"   ... +{score - 10} more")

            print("\n--------------------------")

    # -------------------------
    # SINGLE NODE TRACE
    # -------------------------
    def trace_single(self, node):
        impact = self.trace_impact(node)

        print(f"\n🧠 ROOT TRACE: {node}")
        print(f"TOTAL IMPACT: {len(impact)}\n")

        for i in impact[:25]:
            print(f"{node} → {i}")

        if len(impact) > 25:
            print(f"... +{len(impact) - 25} more")


if __name__ == "__main__":
    engine = RootCauseTracerV61()
    engine.scan()
    engine.build_graph()
    engine.report()

    # Example deep trace (edit this)
    engine.trace_single("omega_bus")
