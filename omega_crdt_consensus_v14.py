import time
import random
from collections import defaultdict


# =========================
# 🌐 CRDT VALUE TYPE
# =========================
class CRDTValue:

    def __init__(self, value=0.0, timestamp=None):

        self.value = value
        self.timestamp = timestamp or time.time()

    def merge(self, other):

        # last-write-wins with stability bias
        if other.timestamp > self.timestamp:
            return other

        return self


# =========================
# 🧠 CRDT NODE STATE
# =========================
class CRDTNode:

    def __init__(self, node_id):

        self.id = node_id

        self.state = {
            "strength": CRDTValue(random.random()),
            "reward": CRDTValue(0.0),
            "entropy": CRDTValue(0.5),
        }


    def update(self):

        # local mutation
        self.state["strength"] = CRDTValue(
            self.state["strength"].value + random.uniform(-0.05, 0.05)
        )

        self.state["reward"] = CRDTValue(
            self.state["reward"].value + random.uniform(0, 0.1)
        )

        self.state["entropy"] = CRDTValue(
            max(0.0, min(1.0, self.state["entropy"].value + random.uniform(-0.02, 0.02)))
        )


# =========================
# 🌐 CRDT MERGE ENGINE
# =========================
class CRDTMesh:

    def __init__(self, node_ids):

        self.nodes = {nid: CRDTNode(nid) for nid in node_ids}

        self.global_view = defaultdict(lambda: CRDTValue(0.0))

    # -------------------------
    # MERGE NODE INTO GLOBAL STATE
    # -------------------------
    def merge_node(self, node):

        for k, v in node.state.items():

            if k not in self.global_view:
                self.global_view[k] = v
            else:
                self.global_view[k] = self.global_view[k].merge(v)

    # -------------------------
    # SYNC ALL NODES
    # -------------------------
    def sync(self):

        for node in self.nodes.values():

            self.merge_node(node)

            # push global corrections back
            node.state["entropy"] = self.global_view["entropy"]
            node.state["reward"] = self.global_view["reward"]

    # -------------------------
    # STEP EVOLUTION
    # -------------------------
    def step(self):

        for node in self.nodes.values():
            node.update()

        self.sync()

    # -------------------------
    # STATUS
    # -------------------------
    def status(self):

        return {
            "nodes": len(self.nodes),
            "entropy": self.global_view["entropy"].value,
            "reward": self.global_view["reward"].value,
            "strength": self.global_view["strength"].value
        }


# =========================
# 🚀 DEMO LOOP
# =========================
if __name__ == "__main__":

    mesh = CRDTMesh(["brain_0", "brain_1", "brain_2", "brain_3"])

    tick = 0

    print("[Ω-CRDT v14] consensus system ONLINE")

    while True:

        tick += 1

        mesh.step()

        if tick % 5 == 0:
            print("[Ω-CRDT]", mesh.status())

        time.sleep(0.5)
