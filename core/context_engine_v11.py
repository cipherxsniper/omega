# core/context_engine_v11.py

class ContextEngine:
    def __init__(self):
        self.context = {}
        self.history = []

    def update(self, key, value):
        self.context[key] = value
        self.history.append((key, value))

    def get(self, key):
        return self.context.get(key)

    def snapshot(self):
        return self.context.copy()

    def rewind(self, steps=5):
        return self.history[-steps:]

    def awareness_state(self):
        return {
            "active_keys": list(self.context.keys()),
            "history_depth": len(self.history)
        }
