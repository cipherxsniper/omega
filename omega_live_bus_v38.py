class LiveBus:

    def __init__(self, observer):
        self.nodes = {}
        self.observer = observer

    def register(self, node):
        self.nodes[node] = []

    def send(self, node, message):
        if node not in self.nodes:
            self.register(node)

        self.nodes[node].append(message)
        self.observer.ingest(node, message)

    def broadcast(self, message):
        for node in self.nodes:
            self.send(node, message)
