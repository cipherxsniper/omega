def resolve_dag(services):
    # AUTO-CONVERT LIST → DICT
    if isinstance(services, list):
        services = {s: [] for s in services}

    visited = set()
    order = []

    def visit(node):
        if node in visited:
            return
        visited.add(node)

        for dep in services.get(node, []):
            visit(dep)

        order.append(node)

    for s in services:
        visit(s)

    return order
