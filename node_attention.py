import random
from omega_bus import BUS

class AttentionNode:
    def __init__(self):
        self.bus = BUS

    def step(self, tick):
        signals = self.bus.read()[-20:]

        score = sum(random.random() for _ in signals)

        packet = {
            "type": "attention_signal",
            "tick": tick,
            "score": score,
            "focus": "high" if score > 10 else "low"
        }

        self.bus.write(packet)
        print("[ATTN] tick", tick, "score", round(score, 2))

if __name__ == "__main__":
    import time
    node = AttentionNode()
    t = 0
    while True:
        node.step(t)
        t += 1
        time.sleep(1)
