class ExecutionNode:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn
        self.links = []
        self.health = 1.0

    def connect(self, node):
        self.links.append(node)


class OmegaExecutionGraphV65:
    def __init__(self):
        self.nodes = {}
        self.history = []

    def add_node(self, name, fn):
        self.nodes[name] = ExecutionNode(name, fn)

    # =========================
    # DYNAMIC ROUTING ENGINE
    # =========================
    def route(self, entry, context):
        node = self.nodes.get(entry)

        if not node:
            return {"error": "missing_node"}

        trace = []

        current = node

        while current:
            result = current.fn(context)
            trace.append((current.name, result))

            # =========================
            # SELF-HEALING LOGIC
            # =========================
            if result.get("health", 1.0) < 0.5:
                # degrade link strength
                current.health *= 0.9

                # reroute to safer node if available
                for n in current.links:
                    if n.health > current.health:
                        current = n
                        break
                else:
                    break
            else:
                # continue normal flow
                if current.links:
                    current = current.links[0]
                else:
                    current = None

        self.history.append(trace)

        return {
            "trace": trace,
            "graph_health": self.graph_health()
        }

    def graph_health(self):
        if not self.nodes:
            return 0

        return sum(n.health for n in self.nodes.values()) / len(self.nodes)
