import random
from omega_bus import BUS

class StabilityNode:
    def __init__(self):
        self.bus = BUS

    def step(self, tick):
        data = self.bus.read()[-20:]

        instability = random.uniform(0, 1) + len(data) * 0.001

        packet = {
            "type": "stability",
            "tick": tick,
            "instability": instability
        }

        self.bus.write(packet)
        print("[STABLE] tick", tick, "instability", round(instability, 3))

if __name__ == "__main__":
    import time
    node = StabilityNode()
    t = 0
    while True:
        node.step(t)
        t += 1
        time.sleep(1)
