import socket
import json
import time
import threading
import hashlib
from collections import deque, defaultdict

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmConsciousnessGraphV14:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠🌍 [V14 SWARM CONSCIOUSNESS GRAPH] BOOTING...\n")

        # ----------------------------
        # CRDT MEMORY CORE
        # ----------------------------
        self.memory = get_crdt()

        # ----------------------------
        # NETWORK
        # ----------------------------
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        # ----------------------------
        # STATE
        # ----------------------------
        self.running = True
        self.event_queue = deque()
        self.event_count = 0

        # ----------------------------
        # SWARM GRAPH (NEW CORE)
        # ----------------------------
        self.nodes = {}               # node_id -> metadata
        self.edges = defaultdict(int) # node relationships
        self.trust = defaultdict(lambda: 1.0)

        # ----------------------------
        # THREADS
        # ----------------------------
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.graph_loop, daemon=True).start()

        print(f"🟢 [V14 ONLINE] {self.host}:{self.port}\n")

    # =====================================================
    # NODE IDENTITY
    # =====================================================
    def register_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "first_seen": time.time(),
                "events": 0,
                "trust": 1.0
            }

    # =====================================================
    # LISTEN LOOP
    # =====================================================
    def listen_loop(self):
        print("[V14] LISTENING...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                try:
                    event = json.loads(data.decode("utf-8"))
                except:
                    continue

                node_id = event.get("node_id", str(addr))
                self.register_node(node_id)

                self.event_queue.append(event)

            except Exception as e:
                print("[V14 LISTEN ERROR]", e)

    # =====================================================
    # PROCESSOR (CONSCIOUSNESS INTAKE)
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if not self.event_queue:
                    time.sleep(0.01)
                    continue

                event = self.event_queue.popleft()
                self.event_count += 1

                node_id = event.get("node_id", "unknown")
                self.nodes[node_id]["events"] += 1

                # ----------------------------
                # UPDATE GRAPH EDGES
                # ----------------------------
                self._update_graph(node_id, event)

                # ----------------------------
                # WRITE TO CRDT MEMORY
                # ----------------------------
                try:
                    self.memory.store(event)
                except:
                    self.memory.apply(event)

                print(f"[V14 EVENT] {node_id} → {event}")

            except Exception as e:
                print("[V14 PROCESS ERROR]", e)

    # =====================================================
    # GRAPH ENGINE (CORE "CONSCIOUSNESS")
    # =====================================================
    def _update_graph(self, node_id, event):
        content = event.get("content", "")

        key = f"{node_id}:{content}"

        self.edges[key] += 1

        # trust drift logic
        if "error" in content.lower():
            self.trust[node_id] -= 0.01
        else:
            self.trust[node_id] += 0.001

        # clamp trust
        self.trust[node_id] = max(0.1, min(2.0, self.trust[node_id]))

        self.nodes[node_id]["trust"] = self.trust[node_id]

    # =====================================================
    # GRAPH INTROSPECTION LOOP
    # =====================================================
    def graph_loop(self):
        while self.running:
            try:
                time.sleep(5)

                print("\n🌍 [V14 SWARM GRAPH STATE]")
                print(f"events: {self.event_count}")
                print(f"nodes: {len(self.nodes)}")

                top_nodes = sorted(
                    self.nodes.items(),
                    key=lambda x: x[1]["events"],
                    reverse=True
                )[:3]

                print("top nodes:")
                for n, data in top_nodes:
                    print(f" - {n} | trust={data['trust']:.2f} | events={data['events']}")

                print("──────────────────────────────\n")

            except Exception as e:
                print("[V14 GRAPH ERROR]", e)


# =====================================================
# BOOT
# =====================================================
if __name__ == "__main__":
    bus = SwarmConsciousnessGraphV14()

    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("\n[V14 SHUTDOWN]")
        bus.running = False
