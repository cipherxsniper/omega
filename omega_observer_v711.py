from omega_language_v711 import OmegaLanguageV711
from omega_memory_v711 import OmegaMemoryV711

class OmegaObserverV711:

    def __init__(self):
        self.lang = OmegaLanguageV711()
        self.memory = OmegaMemoryV711()

    def process(self, event):

        memory_view = self.memory.recent()

        narration = self.lang.render(event, memory_view)

        self.memory.store(event, narration)

        return narration

    def introspect(self, tick):

        return {
            "event_type": "self_reflection",
            "source": "observer",
            "raw": f"tick={tick}",
            "system_state": {},
            "severity": 0.3
        }

# === Ω v7.11 EVENT GUARD (PREVENT None EVENTS) ===
def safe_event(event):
    if event is None:
        return {
            "event_type": "null_event",
            "source": "system",
            "raw": "None event intercepted",
            "interpretation": "No execution output was produced this tick",
            "system_state": {},
            "severity": 0.2
        }
    return event

