from collections import defaultdict, deque

class OmegaDAGEngineV3:
    def resolve(self, services):
        graph = defaultdict(list)
        indeg = defaultdict(int)

        for s in services:
            for dep in s.get("requires", []):
                graph[dep].append(s["name"])
                indeg[s["name"]] += 1

        q = deque([s["name"] for s in services if indeg[s["name"]] == 0])
        order = []

        while q:
            n = q.popleft()
            order.append(n)

            for nxt in graph[n]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)

        return order
