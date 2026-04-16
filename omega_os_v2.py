import threading
import queue
import random
import time
import json
import os


# =========================================================
# GLOBAL MESSAGE BUS
# =========================================================
class MessageBus:
    def __init__(self):
        self.queues = {}

    def register(self, node_id):
        self.queues[node_id] = queue.Queue()

    def send(self, to, msg):
        if to in self.queues:
            self.queues[to].put(msg)

    def broadcast(self, msg):
        for q in self.queues.values():
            q.put(msg)


BUS = MessageBus()


# =========================================================
# PERSISTENT MEMORY
# =========================================================
class MemoryStore:
    def __init__(self, path="omega_state.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except:
                pass

        return {
            "node_scores": {},
            "idea_scores": {},
            "history": []
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)


# =========================================================
# NODE (INDEPENDENT AGENT)
# =========================================================
class Node(threading.Thread):
    def __init__(self, node_id, memory: MemoryStore):
        super().__init__()
        self.node_id = node_id
        self.memory = memory
        self.energy = random.uniform(0.8, 1.2)
        self.ideas = ["entropy", "memory", "gravity"]

        BUS.register(node_id)

    # -------------------------
    # PROCESS MESSAGES
    # -------------------------
    def process_message(self, msg):
        if msg["type"] == "idea_boost":
            idea = msg["payload"]
            self.ideas.append(idea)
            self.energy += 0.05

    # -------------------------
    # THINK LOOP
    # -------------------------
    def run(self):
        while True:
            try:
                msg = BUS.queues[self.node_id].get(timeout=0.2)
                self.process_message(msg)
            except:
                pass

            # cognitive drift
            self.energy += random.uniform(-0.02, 0.03)

            if self.energy < 0.3:
                self.energy += 0.1  # recovery pressure

            # generate idea
            if random.random() < 0.2:
                idea = random.choice(self.ideas)

                target = random.choice(list(BUS.queues.keys()))
                BUS.send(target, {
                    "from": self.node_id,
                    "to": target,
                    "type": "idea_boost",
                    "payload": idea
                })

            time.sleep(0.1)


# =========================================================
# OMEGA OS KERNEL v2
# =========================================================
class OmegaOSv2:
    def __init__(self):
        self.memory = MemoryStore()
        self.nodes = []

    def spawn_nodes(self, n=4):
        for i in range(n):
            node = Node(f"node_{i}", self.memory)
            self.nodes.append(node)

    def run(self):
        print("[Ω-OS v2] Distributed Cognition Kernel ONLINE")

        self.spawn_nodes(5)

        for n in self.nodes:
            n.start()

        # kernel loop (monitor + persistence)
        tick = 0
        while True:
            tick += 1

            snapshot = {
                "tick": tick,
                "energy": [n.energy for n in self.nodes],
                "avg_energy": sum(n.energy for n in self.nodes) / len(self.nodes)
            }

            self.memory.state["history"].append(snapshot)

            # lightweight learning signal
            for n in self.nodes:
                self.memory.state["node_scores"][n.node_id] = n.energy

            if tick % 10 == 0:
                self.memory.save()
                print(f"[Ω-OS v2] tick={tick} avg_energy={snapshot['avg_energy']:.3f}")

            time.sleep(1)


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    OmegaOSv2().run()
