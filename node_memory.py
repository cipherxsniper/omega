import random
from omega_bus import BUS

class MemoryNode:
    def __init__(self):
        self.bus = BUS
        self.memory = []

    def step(self, tick):
        recent = self.bus.read()[-10:]

        for item in recent:
            if item.get("type") == "signal":
                self.memory.append(item)

        packet = {
            "type": "memory_update",
            "tick": tick,
            "memory_size": len(self.memory),
            "drift": random.uniform(0, 1)
        }

        self.bus.write(packet)
        print("[MEM] tick", tick, "size", len(self.memory))

if __name__ == "__main__":
    import time
    node = MemoryNode()
    t = 0
    while True:
        node.step(t)
        t += 1
        time.sleep(1)
