import os
import ast

ROOTS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

def get_py_files():
    files = []
    for r in ROOTS:
        for root, _, f in os.walk(r):
            for file in f:
                if file.endswith(".py"):
                    files.append(os.path.join(root, file))
    return files

def parse_imports(file_path):
    try:
        with open(file_path, "r", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return imports

    except:
        return []

def build_graph():
    graph = {}

    files = get_py_files()

    for f in files:
        graph[f] = parse_imports(f)

    return graph

if __name__ == "__main__":
    g = build_graph()
    print("🧠 Omega Dependency Graph Built")
    print("Nodes:", len(g))
