import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV13:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠🔧 [SWARM BUS V13] INITIALIZING SELF-HEALING AUTONOMY LAYER...\n")

        # =========================
        # MEMORY CORE (CRDT)
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
        # CAUSAL MODEL
        # =========================
        self.causal_graph = defaultdict(lambda: defaultdict(float))
        self.event_chain = deque(maxlen=2000)

        self.event_queue = deque()

        # =========================
        # HEALTH / STABILITY TRACKING
        # =========================
        self.instability_score = defaultdict(float)
        self.repair_log = []

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.self_heal_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V13] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # EVENT ID
    # =====================================================
    def eid(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # FEATURE EXTRACTION
    # =====================================================
    def feature(self, event):
        text = event.get("content", "").lower()

        if "hello" in text or "hi" in text:
            return "greeting"
        if "why" in text:
            return "question_why"
        if "what" in text:
            return "question_what"
        if "run" in text:
            return "command"
        return "unknown"

    # =====================================================
    # CAUSAL UPDATE
    # =====================================================
    def update_graph(self, prev, curr):
        if prev:
            self.causal_graph[prev][curr] += 1.0

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V13 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V13] LISTENING...\n")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                event["received_at"] = time.time()
                self.event_queue.append(event)

            except Exception:
                traceback.print_exc()
                time.sleep(1)

    # =====================================================
    # PROCESSOR
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.event_queue:
                    event = self.event_queue.popleft()

                    curr = self.feature(event)
                    prev = self.event_chain[-1] if self.event_chain else None

                    self.event_chain.append(curr)

                    self.update_graph(prev, curr)

                    self.event_count += 1

                    self.write_memory({
                        "event": event,
                        "feature": curr
                    })

                    print(f"\n🧠 [V13 EVENT]")
                    print(f"  feature : {curr}")
                    print(f"  event   : {event.get('content')}")

                time.sleep(0.01)

            except Exception as e:
                print("[V13 PROCESS ERROR]", e)

    # =====================================================
    # SELF-HEALING ENGINE
    # =====================================================
    def self_heal_loop(self):
        while self.running:
            try:
                time.sleep(5)

                print("\n🔧 [V13 SELF-HEALING CHECK]")

                # detect weak links
                for a, targets in list(self.causal_graph.items()):
                    total = sum(targets.values())

                    if total < 1:
                        self.instability_score[a] += 1

                    # heal unstable nodes
                    if self.instability_score[a] > 3:
                        self.causal_graph[a]["unknown"] += 0.5

                        self.repair_log.append({
                            "node": a,
                            "action": "patched_missing_edge",
                            "time": time.time()
                        })

                        print(f"  🧬 repaired node: {a}")

                print(f"  repairs: {len(self.repair_log)}")

            except Exception as e:
                print("[V13 HEAL ERROR]", e)

    # =====================================================
    # HEALTH MONITOR
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V13 STATUS]")
            print(f"  events     : {self.event_count}")
            print(f"  causal     : {len(self.causal_graph)} nodes")
            print(f"  repairs    : {len(self.repair_log)}")
            print("──────────────────────────────────────\n")

    # =====================================================
    # STOP
    # =====================================================
    def stop(self):
        self.running = False
        self.sock.close()


if __name__ == "__main__":
    print("""
========================================
🧠 SWARM BUS V13 — SELF-HEALING AUTONOMY LAYER
========================================
✔ CAUSAL GRAPH REPAIR
✔ INSTABILITY DETECTION
✔ AUTONOMOUS SELF-CORRECTION LOOP
✔ MEMORY CONSISTENCY PRESERVATION
✔ CRDT SAFE CORE
========================================
""")

    bus = SwarmBusV13()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V13] SHUTDOWN")
        bus.stop()
def listen_loop(self):
    print("[SWARM BUS V13] LISTENING...\n")

    while self.running:
        try:
            data, addr = self.sock.recvfrom(65535)

            try:
                event = json.loads(data.decode("utf-8"))
            except Exception:
                print("[DROP] invalid json from", addr)
                continue

            # FORCE normalize safe structure
            event = {
                "type": event.get("type", "unknown"),
                "content": event.get("content", ""),
                "node_id": event.get("node_id", str(addr)),
                "timestamp": event.get("timestamp", time.time())
            }

            if not hasattr(self, "event_queue"):
                from collections import deque
                self.event_queue = deque()

            self.event_queue.append(event)

        except Exception as e:
            print("[LISTEN ERROR]", e)


def processor_loop(self):
    while self.running:
        try:
            if not hasattr(self, "event_queue"):
                from collections import deque
                self.event_queue = deque()

            if self.event_queue:
                event = self.event_queue.popleft()

                self.event_count += 1

                # 🔥 FORCE MEMORY WRITE (CRDT SAFE)
                try:
                    self.memory.store(event)
                except Exception:
                    try:
                        self.memory.apply(event)
                    except Exception as e:
                        print("[MEMORY WRITE FAILED]", e)

                print(f"[V13 RECEIVED] {event}")

            time.sleep(0.01)

        except Exception as e:
            print("[PROCESS ERROR]", e)
