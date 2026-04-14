# core/memory_graph_v2.py

class MemoryGraph:
    def __init__(self, shared_state):
        self.state = shared_state

    def link(self, key, value):
        graph = self.state["knowledge_graph"]

        if key not in graph:
            graph[key] = []

        graph[key].append(value)

    def build(self):
        for entry in self.state["memory"][-10:]:
            self.link(entry["tag"], str(entry["data"]))

    def stats(self):
        graph = self.state["knowledge_graph"]
        return {
            "nodes": len(graph),
            "connections": sum(len(v) for v in graph.values())
        }
