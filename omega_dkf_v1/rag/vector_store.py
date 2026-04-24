class VectorStore:
    def __init__(self):
        self.store = []

    def add(self, vector):
        self.store.append(vector)
