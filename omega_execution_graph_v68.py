class Node:
    def __init__(self, fn):
        self.fn = fn
        self.edges = []

    def connect(self, node):
        self.edges.append(node)


class OmegaExecutionGraphV68:
    def __init__(self):
        self.nodes = {}
        self.repair_node = None

    def add_node(self, name, fn):
        self.nodes[name] = Node(fn)

    def set_repair_node(self, fn):
        self.repair_node = fn

    def connect(self, a, b):
        self.nodes[a].connect(self.nodes[b])

    def route(self, start, memory, payload):
        current = self.nodes[start]

        results = []

        while current:
            result = current.fn(memory, payload)

            # CONTRACT ENFORCEMENT
            if not isinstance(result, dict):
                raise ValueError("Node violated contract")

            if "health" not in result:
                raise ValueError("Missing health field")

            results.append(result)

            # AUTO-REPAIR CONDITION
            if result["health"] < 0.5 and self.repair_node:
                repair_result = self.repair_node(memory, payload)
                results.append(repair_result)

            if current.edges:
                current = current.edges[0]
            else:
                current = None

        return {
            "graph_results": results,
            "final_health": results[-1]["health"] if results else 0.0
        }
