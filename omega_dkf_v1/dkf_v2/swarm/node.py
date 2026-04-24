class SwarmNode:
    def __init__(self, node_id, role="reasoner"):
        self.node_id = node_id
        self.role = role
        self.state = {}
        self.inbox = []

    def receive(self, message):
        self.inbox.append(message)

    def think(self):
        if not self.inbox:
            return None

        msg = self.inbox.pop(0)
        return {
            "node": self.node_id,
            "role": self.role,
            "output": f"processed({msg})"
        }
