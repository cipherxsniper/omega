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
