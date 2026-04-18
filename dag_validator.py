import ast

def build_dependency_graph(files):
    graph = {}

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file)

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            graph[file] = imports

        except Exception as e:
            graph[file] = {"error": str(e)}

    return graph


def validate_graph(graph):
    issues = []

    for node, edges in graph.items():
        if isinstance(edges, dict) and "error" in edges:
            issues.append({
                "type": "parse_error",
                "node": node,
                "error": edges["error"]
            })

        elif isinstance(edges, list):
            if len(edges) == 0:
                issues.append({
                    "type": "orphan_node",
                    "node": node
                })

    return issues
