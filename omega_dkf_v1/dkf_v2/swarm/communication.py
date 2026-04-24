class SwarmBus:
    def __init__(self):
        self.channels = {}

    def subscribe(self, channel, node):
        self.channels.setdefault(channel, []).append(node)

    def emit(self, channel, message):
        for node in self.channels.get(channel, []):
            node.receive(message)
