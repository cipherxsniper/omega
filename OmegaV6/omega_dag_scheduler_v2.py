from collections import defaultdict, deque

class OmegaDAGSchedulerV2:
    def build(self, units):
        graph = defaultdict(list)
        indeg = defaultdict(int)

        for u in units:
            for dep in u.get("requires", []):
                graph[dep].append(u["name"])
                indeg[u["name"]] += 1

        q = deque([u["name"] for u in units if indeg[u["name"]] == 0])
        order = []

        while q:
            n = q.popleft()
            order.append(n)

            for nxt in graph[n]:
                indeg[nxt] -= 1
                if indeg[nxt] == 0:
                    q.append(nxt)

        return order
