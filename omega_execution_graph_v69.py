# OmegaExecutionGraphV69 - Tick Controlled Version

class OmegaExecutionGraphV69:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.repair_node = None
        self.last_tick = None

    def add_node(self, name, fn):
        self.nodes[name] = fn
        self.edges.setdefault(name, [])

    def connect(self, a, b):
        self.edges.setdefault(a, []).append(b)

    def set_repair_node(self, fn):
        self.repair_node = fn

    def route(self, start_node, memory, payload, tick_id=None):

        if self.last_tick == tick_id:
            return {"error": "duplicate_tick_blocked"}

        self.last_tick = tick_id

        graph_results = []

        node = self.nodes[start_node]
        result = node(memory, payload)

        graph_results.append({"node": start_node, **result})

        for next_node in self.edges.get(start_node, []):
            next_result = self.nodes[next_node](memory, payload)
            graph_results.append({"node": next_node, **next_result})

        final_health = graph_results[-1].get("health", 0.0)

        return {
            "tick_id": tick_id,
            "graph_results": graph_results,
            "final_health": final_health
        }
