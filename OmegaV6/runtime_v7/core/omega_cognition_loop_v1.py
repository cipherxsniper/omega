import time
from runtime_v7.core.omega_memory_graph_v3 import get_memory


class OmegaCognitionLoop:
    def __init__(self):
        self.mem = get_memory()
        self.running = True
        self.last_seen = 0

    def think(self):
        events = self.mem.memory.get("events", [])

        new_events = events[self.last_seen:]
        self.last_seen = len(events)

        thoughts = []

        for e in new_events:
            t = e.get("type")

            if t == "heartbeat":
                thoughts.append("Detected system pulse.")
            else:
                thoughts.append(f"Observed event: {t}")

        return thoughts

    def run(self):
        print("[OMEGA COGNITION] LOOP ONLINE")

        while self.running:
            thoughts = self.think()

            for t in thoughts:
                print(f"[THOUGHT] {t}")

            time.sleep(2)


if __name__ == "__main__":
    OmegaCognitionLoop().run()
