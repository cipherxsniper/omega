import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV6:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️ [SWARM BUS V6] INITIALIZING COGNITIVE MEMORY GRAPH...\n")

        # =========================
        # CRDT MEMORY CORE
        # =========================
        self.memory = get_crdt()

        # =========================
        # NETWORK
        # =========================
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        # =========================
        # STATE
        # =========================
        self.running = True
        self.event_count = 0

        # =========================
        # GRAPH MEMORY (NEW IN V6)
        # =========================
        self.nodes = {}        # event_id → node
        self.edges = defaultdict(list)  # node_id → connections

        # pattern memory
        self.pattern_counts = defaultdict(int)

        # queue
        self.queue = deque()

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V6] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # HASH EVENT
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # GRAPH NODE CREATION
    # =====================================================
    def create_node(self, event):
        return {
            "id": self.event_id(event),
            "type": event.get("type"),
            "content": event.get("content"),
            "node_id": event.get("node_id"),
            "timestamp": event.get("timestamp", time.time()),
            "weight": 1.0
        }

    # =====================================================
    # GRAPH LINKING
    # =====================================================
    def link_nodes(self, node):
        nid = node["id"]

        # link by node_id
        node_key = node["node_id"]

        for other_id, other in self.nodes.items():
            if other["node_id"] == node_key:
                self.edges[nid].append(other_id)
                self.edges[other_id].append(nid)

        # link by type similarity
        for other_id, other in self.nodes.items():
            if other["type"] == node["type"]:
                self.edges[nid].append(other_id)

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V6 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V6] LISTENING FOR COGNITIVE EVENTS...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                event["received_at"] = time.time()
                self.queue.append(event)

            except Exception:
                traceback.print_exc()
                time.sleep(1)

    # =====================================================
    # PROCESSOR (GRAPH BUILDER)
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.queue:
                    event = self.queue.popleft()

                    node = self.create_node(event)
                    nid = node["id"]

                    self.nodes[nid] = node

                    # link into graph
                    self.link_nodes(node)

                    # pattern tracking
                    self.pattern_counts[node["type"]] += 1

                    self.event_count += 1

                    print(f"\n[V6 NODE CREATED] {nid}")
                    print(f"[TYPE] {node['type']} | [NODE] {node['node_id']}")
                    print(f"[GRAPH SIZE] nodes={len(self.nodes)} edges={sum(len(v) for v in self.edges.values())}")

                    # write to CRDT memory
                    self.write_memory(node)

                time.sleep(0.01)

            except Exception as e:
                print("[V6 PROCESS ERROR]", e)

    # =====================================================
    # BASIC INSIGHT ENGINE
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V6 COGNITIVE STATUS]")
            print(f"  events_processed : {self.event_count}")
            print(f"  total_nodes      : {len(self.nodes)}")
            print(f"  total_edges      : {sum(len(v) for v in self.edges.values())}")
            print(f"  pattern_counts   : {dict(self.pattern_counts)}")
            print(f"  memory_events    : {len(self.memory.state.get('events', []))}")
            print("──────────────────────────────────────\n")

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        self.running = False
        self.sock.close()


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    print("""
========================================
🧠 SWARM BUS V6 — COGNITIVE GRAPH CORE
========================================
✔ EVENT → NODE TRANSFORMATION
✔ RELATIONSHIP GRAPH BUILDING
✔ TYPE + TEMPORAL LINKING
✔ CRDT MEMORY INTEGRATION
✔ UDP: 0.0.0.0:6100
========================================
""")

    bus = SwarmBusV6()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V6] SHUTDOWN")
        bus.stop()
