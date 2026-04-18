from collections import defaultdict

class EventGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def link(self, source, target):
        self.graph[source].add(target)

    def snapshot(self):
        return {k: list(v) for k, v in self.graph.items()}
