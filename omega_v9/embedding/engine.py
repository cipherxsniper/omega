import numpy as np

class EmbeddingEngine:
    def encode(self, text):
        vec = np.zeros(32)

        for i, c in enumerate(text[:32]):
            vec[i % 32] += ord(c) / 255

        return vec

    def similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)
