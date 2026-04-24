class SwarmMesh:
    def __init__(self):
        self.nodes = {}

    def register(self, node):
        self.nodes[node.node_id] = node

    def broadcast(self, message):
        for node in self.nodes.values():
            node.receive(message)

    def step(self):
        outputs = []
        for node in self.nodes.values():
            result = node.think()
            if result:
                outputs.append(result)
        return outputs
