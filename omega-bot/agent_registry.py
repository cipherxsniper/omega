class AgentRegistry:

    def __init__(self):
        self.nodes = {}
        self.links = {}

    def register(self, node):

        self.nodes[node["name"]] = node

    def connect(self, a, b):

        if a not in self.links:
            self.links[a] = []

        self.links[a].append(b)

    def get_graph(self):
        return {
            "nodes": self.nodes,
            "links": self.links
        }
