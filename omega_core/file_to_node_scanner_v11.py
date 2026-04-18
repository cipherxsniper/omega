import os

class FileNodeScanner:

    def scan(self, root="~/Omega"):
        root = os.path.expanduser(root)

        nodes = []

        for r, d, f in os.walk(root):
            for file in f:
                if file.endswith(".py"):
                    nodes.append(file.replace(".py",""))

        return list(set(nodes))
