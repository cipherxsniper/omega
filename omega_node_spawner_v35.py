import os

class NodeSpawner:

    def __init__(self, root="."):
        self.root = root

    def create_node(self, name, logic):
        path = os.path.join(self.root, name)

        with open(path, "w") as f:
            f.write(logic)

        return f"Node created: {name}"

    def suggest_new_node(self, pattern):
        return f"Suggested node based on pattern: {pattern}"
