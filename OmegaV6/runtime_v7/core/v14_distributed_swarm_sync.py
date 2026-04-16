import socket
import json
import time
import threading
from collections import defaultdict


class DistributedSwarmSyncV14:
    """
    V14 Distributed Swarm Synchronization Layer

    Enables:
    - multi-device memory sync
    - LAN event propagation
    - shared swarm state graph
    """

    def __init__(self, port=7014):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = f"node-{int(time.time())}"

        # GLOBAL SWARM STATE (merged across nodes)
        self.global_graph = defaultdict(dict)

        # dedup across network
        self.seen_events = set()

        self.running = True

        print(f"[V14 SYNC] ONLINE | node={self.node_id} | port={self.port}")

    # -----------------------------
    # BROADCAST EVENT
    # -----------------------------
    def broadcast(self, event):
        payload = json.dumps(event).encode()

        # LAN broadcast (simple local loop simulation)
        self.sock.sendto(payload, ("127.0.0.1", self.port))

    # -----------------------------
    # RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                event = json.loads(data.decode())

                print(f"[V14 EVENT] {event}")

                event_id = self._event_id(event)

                if event_id in self.seen_events:
                    continue

                self.seen_events.add(event_id)

                self._merge_event(event)

            except Exception as e:
                print(f"[V14 ERROR] {e}")

    # -----------------------------
    # EVENT ID (DEDUP KEY)
    # -----------------------------
    def _event_id(self, event):
        return f"{event.get('node_id')}:{event.get('type')}:{event.get('timestamp')}"

    # -----------------------------
    # MERGE INTO GLOBAL GRAPH
    # -----------------------------
    def _merge_event(self, event):
        node = event.get("node_id")

        if node not in self.global_graph:
            self.global_graph[node] = {
                "events": [],
                "last_seen": time.time()
            }

        self.global_graph[node]["events"].append(event)
        self.global_graph[node]["last_seen"] = time.time()

    # -----------------------------
    # SWARM STATE VIEW
    # -----------------------------
    def get_swarm_state(self):
        return {
            "nodes": len(self.global_graph),
            "total_events": sum(len(v["events"]) for v in self.global_graph.values())
        }

    # -----------------------------
    # HEARTBEAT SYNC
    # -----------------------------
    def heartbeat(self):
        while self.running:
            event = {
                "node_id": self.node_id,
                "type": "heartbeat",
                "timestamp": time.time()
            }

            self.broadcast(event)

            time.sleep(3)

    # -----------------------------
    # START ENGINE
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V14 SYNC] STARTED")

        while True:
            state = self.get_swarm_state()
            print(f"[V14 STATE] nodes={state['nodes']} events={state['total_events']}")
            time.sleep(5)


# -----------------------------
# FACTORY
# -----------------------------
def create_swarm_sync():
    return DistributedSwarmSyncV14()


if __name__ == "__main__":
    create_swarm_sync().start()
