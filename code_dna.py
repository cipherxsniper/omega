import hashlib
import random

class CodeDNA:
    def encode(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def mutate(self, text):
        lines = text.split("\n")

        idx = random.randint(0, len(lines)-1)
        lines[idx] = lines[idx][::-1]  # reverse mutation

        return "\n".join(lines)

    def crossover(self, a, b):
        split = len(a)//2
        return a[:split] + b[split:]
