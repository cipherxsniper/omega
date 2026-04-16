import time
import threading
import queue

class OmegaBus:
    def __init__(self):
        self.q = queue.Queue()
        self.subs = []
        self.memory = []

    def publish(self, event):
        self.q.put(event)

    def subscribe(self, node):
        self.subs.append(node)

    def loop(self):
        while True:
            if not self.q.empty():
                event = self.q.get()
                self.memory.append(event)
                for s in self.subs:
                    s.receive(event)
            time.sleep(0.05)


class OmegaNode:
    def __init__(self, name, bus):
        self.name = name
        self.bus = bus
        self.state = {"beliefs": {}, "confidence": 0.5}
        self.bus.subscribe(self)

    def receive(self, event):
        # V13 SELF-MODIFICATION HOOK
        if event["node"] != self.name:
            self.state["confidence"] += 0.01
            self.state["beliefs"][event["node"]] = self.state["beliefs"].get(event["node"], 0) + 1

    def think(self):
        return {
            "node": self.name,
            "confidence": self.state["confidence"]
        }

    def run(self):
        while True:
            self.bus.publish(self.think())
            time.sleep(1)


class OmegaSystem:
    def __init__(self):
        self.bus = OmegaBus()
        self.nodes = [
            OmegaNode("memory", self.bus),
            OmegaNode("swarm", self.bus)
        ]

    def start(self):
        threading.Thread(target=self.bus.loop, daemon=True).start()
        for n in self.nodes:
            threading.Thread(target=n.run, daemon=True).start()

        while True:
            print("GLOBAL EVENTS:", len(self.bus.memory))
            time.sleep(5)

if __name__ == "__main__":
    OmegaSystem().start()
