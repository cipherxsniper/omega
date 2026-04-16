import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV7:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️ [SWARM BUS V7] INITIALIZING CAUSAL INTELLIGENCE ENGINE...\n")

        # =========================
        # MEMORY CORE
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
        # GRAPH STRUCTURES
        # =========================
        self.nodes = {}
        self.edges = defaultdict(list)

        # 🧠 V7: causal graph
        self.causal_edges = defaultdict(list)

        # event sequence memory
        self.recent_events = deque(maxlen=50)

        # causal statistics
        self.cause_score = defaultdict(lambda: defaultdict(float))
        self.transition_count = defaultdict(lambda: defaultdict(int))

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.causal_engine_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V7] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # ID
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # NODE CREATION
    # =====================================================
    def create_node(self, event):
        return {
            "id": self.event_id(event),
            "type": event.get("type"),
            "content": event.get("content"),
            "node_id": event.get("node_id"),
            "timestamp": event.get("timestamp", time.time())
        }

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V7 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V7] LISTENING...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                event["received_at"] = time.time()
                self.recent_events.append(event)

            except Exception:
                traceback.print_exc()
                time.sleep(1)

    # =====================================================
    # PROCESSOR (GRAPH BUILDER)
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.recent_events:
                    event = self.recent_events.popleft()

                    node = self.create_node(event)
                    nid = node["id"]

                    self.nodes[nid] = node

                    # link simple graph edges
                    for other_id in list(self.nodes.keys())[-10:]:
                        if other_id != nid:
                            self.edges[nid].append(other_id)

                    self.event_count += 1

                    self.write_memory(node)

                    print(f"[V7 NODE] {nid} | type={node['type']}")

                time.sleep(0.01)

            except Exception as e:
                print("[V7 PROCESS ERROR]", e)

    # =====================================================
    # CAUSAL ENGINE (CORE UPGRADE)
    # =====================================================
    def causal_engine_loop(self):
        while self.running:
            try:
                if len(self.recent_events) >= 2:

                    prev = self.recent_events[-2]
                    curr = self.recent_events[-1]

                    a = prev.get("type", "unknown")
                    b = curr.get("type", "unknown")

                    # record transition
                    self.transition_count[a][b] += 1

                    # compute causal probability
                    total = sum(self.transition_count[a].values())
                    self.cause_score[a][b] = self.transition_count[a][b] / total

                    # store causal link if strong enough
                    if self.cause_score[a][b] > 0.6:
                        self.causal_edges[a].append(b)

                        print(f"\n🧠 [CAUSAL LEARNED]")
                        print(f"  {a} → {b}")
                        print(f"  confidence={self.cause_score[a][b]:.2f}\n")

                time.sleep(0.5)

            except Exception as e:
                print("[V7 CAUSAL ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V7 STATUS]")
            print(f"  events       : {self.event_count}")
            print(f"  nodes        : {len(self.nodes)}")
            print(f"  causal_links : {sum(len(v) for v in self.causal_edges.values())}")
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
🧠 SWARM BUS V7 — CAUSAL INTELLIGENCE
========================================
✔ EVENT GRAPH BUILDING
✔ TEMPORAL SEQUENCING
✔ CAUSE → EFFECT LEARNING
✔ PROBABILISTIC TRANSITION MODEL
✔ CRDT MEMORY SAFE
========================================
""")

    bus = SwarmBusV7()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V7] SHUTDOWN")
        bus.stop()
