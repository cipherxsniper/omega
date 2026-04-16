class OmegaMemoryV711:

    def __init__(self):
        self.events = []

    def store(self, event, narration):
        self.events.append({
            "event": event,
            "narration": narration
        })

    def recent(self, n=5):
        return self.events[-n:]
