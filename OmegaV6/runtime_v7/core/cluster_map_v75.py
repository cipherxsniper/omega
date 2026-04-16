import json

class ClusterMapV75:
    def __init__(self, registry):
        self.registry = registry

    def export(self, path="cluster_map.json"):
        data = self.registry.snapshot()

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        return path
