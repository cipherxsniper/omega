import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque


from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV12:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️🌍 [SWARM BUS V12] INITIALIZING CAUSAL WORLD INTELLIGENCE ENGINE...\n")

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
        # CAUSAL WORLD MODEL (V12 CORE)
        # =========================
        self.causal_graph = defaultdict(lambda: defaultdict(float))
        self.event_memory = deque(maxlen=2000)

        self.event_queue = deque()

        # statistical tracking
        self.transition_counts = defaultdict(int)

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.causal_learning_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V12] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # HASH
    # =====================================================
    def eid(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # SIMPLE EVENT FEATURE EXTRACTION
    # =====================================================
    def extract_feature(self, event):
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
    # CAUSAL LINK UPDATE
    # =====================================================
    def update_causal_graph(self, prev, curr):
        if prev is None:
            return

        self.causal_graph[prev][curr] += 1.0
        self.transition_counts[(prev, curr)] += 1

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V12 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V12] LISTENING...\n")

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

                    feature = self.extract_feature(event)

                    prev_feature = self.event_memory[-1] if self.event_memory else None

                    self.event_memory.append(feature)

                    # update causal links
                    self.update_causal_graph(prev_feature, feature)

                    self.event_count += 1

                    self.write_memory({
                        "event": event,
                        "feature": feature,
                        "eid": self.eid(event)
                    })

                    print(f"\n🧠 [V12 CAUSAL EVENT]")
                    print(f"  feature : {feature}")
                    print(f"  event   : {event.get('content')}")

                time.sleep(0.01)

            except Exception as e:
                print("[V12 PROCESS ERROR]", e)

    # =====================================================
    # CAUSAL LEARNING LOOP
    # =====================================================
    def causal_learning_loop(self):
        while self.running:
            try:
                time.sleep(5)

                print("\n🌍 [V12 CAUSAL MODEL UPDATE]")

                # show strongest causal links
                strongest = []

                for a, targets in self.causal_graph.items():
                    for b, weight in targets.items():
                        strongest.append((weight, a, b))

                strongest.sort(reverse=True)

                for w, a, b in strongest[:5]:
                    print(f"  {a} → {b}  (strength={w})")

            except Exception as e:
                print("[V12 CAUSAL ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V12 STATUS]")
            print(f"  events        : {self.event_count}")
            print(f"  causal nodes  : {len(self.causal_graph)}")
            print(f"  memory buffer : {len(self.event_memory)}")
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
🧠 SWARM BUS V12 — CAUSAL INTELLIGENCE ENGINE
========================================
✔ CAUSAL GRAPH LEARNING
✔ EVENT SEQUENCING MEMORY
✔ TRANSITION WEIGHTING
✔ WORLD CAUSE-AND-EFFECT MODEL
✔ CRDT SAFE STORAGE
========================================
""")

    bus = SwarmBusV12()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V12] SHUTDOWN")
        bus.stop()
