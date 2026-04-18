class MessageBus:

    def __init__(self):
        self.messages = []

    def send(self, sender, receiver, content):

        self.messages.append({
            "from": sender,
            "to": receiver,
            "content": content
        })

    def broadcast(self, sender, content):

        self.messages.append({
            "from": sender,
            "to": "ALL",
            "content": content
        })

    def fetch(self, receiver):

        return [m for m in self.messages if m["to"] in [receiver, "ALL"]]
