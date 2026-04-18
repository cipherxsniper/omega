import os
import glob
import importlib.util

class NodeRegistry:
    def __init__(self, root="~/Omega"):
        self.root = os.path.expanduser(root)
        self.nodes = []

    def scan(self):
        self.nodes = glob.glob(self.root + "/**/*.py", recursive=True)
        return self.nodes

    def summary(self):
        return {
            "total_nodes": len(self.nodes),
            "active_view": self.nodes[:10]
        }

    def broadcast(self, message_bus):
        for n in self.nodes:
            message_bus.append({"node": n, "msg": "sync"})
