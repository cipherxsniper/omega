import time
import json
import threading
from collections import defaultdict, deque

# -------------------------
# GLOBAL SHARED COGNITIVE STATE
# -------------------------
class SharedMemory:
    def __init__(self):
        self.state = {
            "global_beliefs": {},
            "event_history": [],
            "node_scores": {}
        }

    def update_belief(self, key, value):
        self.state["global_beliefs"][key] = value

    def log_event(self, event):
        self.state["event_history"].append(event)
        if len(self.state["event_history"]) > 500:
            self.state["event_history"].pop(0)


# -------------------------
# COGNITIVE NODE
# -------------------------
class CognitiveNode:
    def __init__(self, node_id):
        self.id = node_id
        self.local_state = {
            "energy": 1.0,
            "confidence": 0.5,
            "specialization": {}
        }

    def process(self, event, memory):

        # simple adaptive reinforcement signal
        load = event.get("load", 0.5)

        if load > 0.7:
            self.local_state["energy"] -= 0.05
            signal = "stress"
        else:
            self.local_state["energy"] += 0.02
            signal = "stable"

        self.local_state["energy"] = max(0.0, min(1.0, self.local_state["energy"]))

        memory.update_belief(self.id, self.local_state["energy"])

        return {
            "node": self.id,
            "signal": signal,
            "energy": self.local_state["energy"],
            "event": event
        }


# -------------------------
# COGNITIVE MESH BUS
# -------------------------
class CognitiveMesh:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.queue = deque()
        self.running = True

        self.memory = SharedMemory()
        self.nodes = {}

    # register node into mesh
    def register_node(self, node):
        self.nodes[node.id] = node

    # pub
    def publish(self, event_type, data):
        self.queue.append((event_type, data))

    # sub
    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)

    # core propagation engine
    def _loop(self):
        while self.running:
            if self.queue:
                event_type, data = self.queue.popleft()

                self.memory.log_event({
                    "type": event_type,
                    "data": data,
                    "ts": time.time()
                })

                # broadcast to subscribers
                for cb in self.subscribers.get(event_type, []):
                    cb(data)

                # cognitive node processing layer
                if event_type == "node.tick":
                    node_id = data["node"]
                    if node_id in self.nodes:
                        result = self.nodes[node_id].process(data, self.memory)
                        self.publish("node.reinforcement", result)

            time.sleep(0.03)

    def start(self):
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()
        return t


# GLOBAL MESH
MESH = CognitiveMesh()
MESH.start()
