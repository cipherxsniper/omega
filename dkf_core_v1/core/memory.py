class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, text):
        self.history.append({"role": role, "text": text})

    def build_context(self):
        return "\n".join([f"{m['role']}: {m['text']}" for m in self.history[-10:]])
