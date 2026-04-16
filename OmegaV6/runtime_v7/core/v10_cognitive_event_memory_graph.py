import time
import json
import threading


class CognitiveEventMemoryGraphV10:
    """
    V10 Cognitive Memory Graph

    Turns swarm events into:
    - persistent memory nodes
    - linked causal graph
    - retrievable intelligence structure
    """

    def __init__(self):
        # node_id -> event node
        self.nodes = {}

        # node_id -> [connected node_ids]
        self.edges = {}

        # simple causal index (type-based linking)
        self.type_index = {}

        self.running = True

        print("[V10 MEMORY GRAPH] ONLINE")

    # -----------------------------
    # CREATE MEMORY NODE
    # -----------------------------
    def add_event(self, event: dict):
        node_id = self._generate_node_id(event)

        node = {
            "id": node_id,
            "event": event,
            "timestamp": event.get("timestamp", time.time()),
            "type": event.get("type"),
            "node_id": event.get("node_id"),
        }

        self.nodes[node_id] = node

        # index by type
        event_type = node["type"]
        self.type_index.setdefault(event_type, []).append(node_id)

        # build causal links
        self._link_node(node_id, node)

        print(f"[V10 MEMORY] node_created={node_id}")

        return node_id

    # -----------------------------
    # CAUSAL LINKING ENGINE
    # -----------------------------
    def _link_node(self, node_id, node):
        event_type = node["type"]

        # link same-type events (temporal chain)
        similar_nodes = self.type_index.get(event_type, [])

        if len(similar_nodes) > 1:
            prev = similar_nodes[-2]
            self._add_edge(prev, node_id, relation="same_type_sequence")

        # link to last known event (global chain)
        if len(self.nodes) > 1:
            last_node = list(self.nodes.keys())[-2]
            self._add_edge(last_node, node_id, relation="temporal_next")

    # -----------------------------
    # ADD EDGE
    # -----------------------------
    def _add_edge(self, a, b, relation="causal"):
        self.edges.setdefault(a, []).append({
            "to": b,
            "relation": relation,
            "timestamp": time.time()
        })

    # -----------------------------
    # NODE ID GENERATION
    # -----------------------------
    def _generate_node_id(self, event):
        return f"{event.get('node_id')}::{event.get('type')}::{int(time.time()*1000)}"

    # -----------------------------
    # QUERY SYSTEM
    # -----------------------------
    def get_by_type(self, event_type):
        return [self.nodes[n] for n in self.type_index.get(event_type, [])]

    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def get_connections(self, node_id):
        return self.edges.get(node_id, [])

    # -----------------------------
    # MEMORY STREAM (optional integration with bus)
    # -----------------------------
    def ingest_stream(self, event_stream):
        for event in event_stream:
            self.add_event(event)


# -----------------------------
# SINGLETON MEMORY GRAPH
# -----------------------------
_GLOBAL_MEMORY = None


def get_memory():
    global _GLOBAL_MEMORY
    if _GLOBAL_MEMORY is None:
        _GLOBAL_MEMORY = CognitiveEventMemoryGraphV10()
    return _GLOBAL_MEMORY


# -----------------------------
# TEST MODE
# -----------------------------
if __name__ == "__main__":
    mem = get_memory()

    mem.add_event({
        "node_id": "testA",
        "type": "heartbeat",
        "timestamp": time.time()
    })

    mem.add_event({
        "node_id": "testB",
        "type": "heartbeat",
        "timestamp": time.time()
    })

    mem.add_event({
        "node_id": "testC",
        "type": "routing_tick",
        "timestamp": time.time()
    })

    print("[V10 TEST] nodes =", len(mem.nodes))

def start():
    print("[V10] STARTED PERSISTENT LOOP")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    import time
    start()

