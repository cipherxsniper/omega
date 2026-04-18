from core.omega_global_memory import OmegaGlobalMemory

GLOBAL_MEMORY = OmegaGlobalMemory()

class OmegaBrain:

    def __init__(self, brain_id):
        self.id = brain_id
        self.vx = 0.0
        self.vy = 0.0

    def perceive(self, events):
        self.vx = sum(e.get("x", 0) for e in events)
        self.vy = sum(e.get("y", 0) for e in events)

    def update(self, events):
        self.perceive(events)

        state = GLOBAL_MEMORY.update(
            self.vx,
            self.vy,
            len(events)
        )

        return {
            "id": self.id,
            "global_memory": state
        }

    def get_state(self):
        return {
            "id": self.id,
            "global_memory": GLOBAL_MEMORY.read()["state"]
        }
