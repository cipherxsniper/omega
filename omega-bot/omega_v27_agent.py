import time

class Agent:

    def __init__(self, node_id, registry, bus):

        self.id = node_id
        self.registry = registry
        self.bus = bus

        self.registry.register(self.id)

    def heartbeat(self):

        self.registry.heartbeat(self.id)

    def think(self, message):

        tokens = message.lower().split()

        return f"{self.id}: processed {len(tokens)} tokens"

    def send(self, receiver, message):

        self.bus.send(self.id, receiver, message)

    def broadcast(self, message):

        self.bus.broadcast(self.id, message)
