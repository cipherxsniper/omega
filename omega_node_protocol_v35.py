class NodeProtocol:

    def __init__(self, memory):
        self.memory = memory

    def send(self, node_name, output):
        # ALL outputs go to truth layer
        self.memory.write(node_name, output)

    def ask(self, question):
        return f"🧠 Omega Question: {question}? Why is this pattern emerging?"
