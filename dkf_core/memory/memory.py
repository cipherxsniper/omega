class Memory:
    def __init__(self):
        self.store = []

    def add(self, role, text):
        self.store.append(f"{role}: {text}")

    def get_context(self, limit=10):
        return "\n".join(self.store[-limit:])
