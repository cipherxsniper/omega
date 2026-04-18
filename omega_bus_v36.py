class OmegaBus:

    def __init__(self):
        self.stream = []

    def broadcast(self, node, message):
        self.stream.append({
            "node": node,
            "message": message
        })

    def read_recent(self, n=10):
        return self.stream[-n:]
