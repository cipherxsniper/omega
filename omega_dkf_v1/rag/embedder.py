class Embedder:
    def embed(self, text):
        return [hash(text) % 1000]
