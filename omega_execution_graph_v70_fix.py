class OmegaExecutionGraphV70_Fixed:
    def __init__(self, base):
        self.base = base

    def _update_weight(self, a, b, health):
        if a not in self.base.edges:
            self.base.edges[a] = {}

        if b not in self.base.edges[a]:
            self.base.edges[a][b] = 1.0

        if health < 0.5:
            self.base.edges[a][b] = max(0.3, self.base.edges[a][b] - 0.1)
        else:
            self.base.edges[a][b] = min(1.0, self.base.edges[a][b] + 0.05)
