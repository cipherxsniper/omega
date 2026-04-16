from collections import defaultdict, deque

class DependencyGraphSchedulerV1:
    def __init__(self):
        self.graph = defaultdict(list)
        self.indegree = defaultdict(int)

    def add(self, module, deps):
        for d in deps:
            self.graph[d].append(module)
            self.indegree[module] += 1

    def resolve(self):
        q = deque([n for n in self.indegree if self.indegree[n] == 0])
        order = []

        while q:
            node = q.popleft()
            order.append(node)

            for nxt in self.graph[node]:
                self.indegree[nxt] -= 1
                if self.indegree[nxt] == 0:
                    q.append(nxt)

        return order
