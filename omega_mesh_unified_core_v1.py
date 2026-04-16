import time
import json
import threading
import queue

# =========================
# 🌐 OMEGA GLOBAL BUS
# =========================

class OmegaBus:
    def __init__(self):
        self.subscribers = {}
        self.global_memory = []
        self.event_queue = queue.Queue()

    def subscribe(self, node_name, callback):
        self.subscribers[node_name] = callback

    def publish(self, event):
        self.event_queue.put(event)

    def broadcast_loop(self):
        while True:
            if not self.event_queue.empty():
                event = self.event_queue.get()

                self.global_memory.append(event)

                for name, callback in self.subscribers.items():
                    callback(event)

            time.sleep(0.05)


# =========================
# 🧠 BASE NODE
# =========================

class OmegaNode:
    def __init__(self, name, bus):
        self.name = name
        self.bus = bus
        self.state = {"beliefs": {}, "confidence": 0.5, "entropy": 1.0}

        bus.subscribe(name, self.receive)

    def receive(self, event):
        # basic learning rule
        if event["node_id"] != self.name:
            self.state["confidence"] += 0.01
            self.state["entropy"] *= 0.99

    def think(self):
        return {
            "node_id": self.name,
            "beliefs": self.state["beliefs"],
            "confidence": self.state["confidence"],
            "entropy": self.state["entropy"],
            "type": "cognition_tick"
        }

    def run(self):
        while True:
            event = self.think()
            self.bus.publish(event)
            time.sleep(1)


# =========================
# 🧠 SPECIALIZED NODES
# =========================

class MemoryNode(OmegaNode):
    def receive(self, event):
        super().receive(event)
        self.state["beliefs"][str(event["node_id"])] = event.get("confidence", 0.5)


class SwarmNode(OmegaNode):
    def receive(self, event):
        super().receive(event)
        self.state["confidence"] *= 1.001


class InternetNode(OmegaNode):
    def think(self):
        # simulate knowledge ingestion
        return {
            "node_id": self.name,
            "beliefs": {"internet_knowledge": 1},
            "confidence": 0.7,
            "entropy": 0.3,
            "type": "knowledge_ingest"
        }


# =========================
# 🚀 ORCHESTRATOR
# =========================

class OmegaSystem:
    def __init__(self):
        self.bus = OmegaBus()

        self.nodes = [
            MemoryNode("memory_core", self.bus),
            SwarmNode("swarm_core", self.bus),
            InternetNode("internet_core", self.bus)
        ]

    def start(self):
        threading.Thread(target=self.bus.broadcast_loop, daemon=True).start()

        for node in self.nodes:
            threading.Thread(target=node.run, daemon=True).start()

        while True:
            print("\n🌐 GLOBAL MEMORY SIZE:", len(self.bus.global_memory))
            time.sleep(5)


# =========================
# 🔥 RUN SYSTEM
# =========================

if __name__ == "__main__":
    system = OmegaSystem()
    system.start()
