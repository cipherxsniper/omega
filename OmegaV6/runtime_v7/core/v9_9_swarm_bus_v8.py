import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV8:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠🌍 [SWARM BUS V8] INITIALIZING SEMANTIC WORLD MODEL...\n")

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
        # SEMANTIC WORLD MODEL (V8 CORE)
        # =========================
        self.world_model = {
            "concepts": {},
            "beliefs": {},
            "entities": {},
            "relations": defaultdict(list)
        }

        # semantic similarity memory
        self.concept_frequency = defaultdict(int)

        # event queue
        self.queue = deque()

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.world_model_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V8] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # HASH
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # SEMANTIC PARSER (CORE V8 UPGRADE)
    # =====================================================
    def interpret_semantics(self, event):
        text = event.get("content", "").lower()

        # simple semantic classification layer (expandable later)
        if any(w in text for w in ["hello", "hi", "hey"]):
            concept = "greeting"
        elif any(w in text for w in ["why", "how", "what"]):
            concept = "question"
        elif any(w in text for w in ["run", "start", "execute"]):
            concept = "command"
        else:
            concept = "unknown_expression"

        return {
            "concept": concept,
            "intent": "interactive",
            "raw": event
        }

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V8 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V8] LISTENING FOR SEMANTIC EVENTS...\n")

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
    # PROCESSOR (SEMANTIC TRANSFORM)
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.queue:
                    event = self.queue.popleft()

                    semantic = self.interpret_semantics(event)

                    concept = semantic["concept"]

                    # update world model
                    self.concept_frequency[concept] += 1
                    self.world_model["concepts"][concept] = {
                        "count": self.concept_frequency[concept],
                        "last_seen": time.time()
                    }

                    # store belief snapshot
                    self.world_model["beliefs"][self.event_id(event)] = semantic

                    self.event_count += 1

                    print(f"\n🧠 [V8 SEMANTIC EVENT]")
                    print(f"  concept : {concept}")
                    print(f"  content : {event.get('content')}")

                    # persist into CRDT memory
                    self.write_memory(semantic)

                time.sleep(0.01)

            except Exception as e:
                print("[V8 PROCESS ERROR]", e)

    # =====================================================
    # WORLD MODEL EVOLUTION
    # =====================================================
    def world_model_loop(self):
        while self.running:
            try:
                time.sleep(5)

                # simple relation inference
                concepts = list(self.world_model["concepts"].keys())

                for i in range(len(concepts) - 1):
                    a = concepts[i]
                    b = concepts[i + 1]

                    self.world_model["relations"][a].append(b)

                print("\n🌍 [V8 WORLD MODEL UPDATE]")
                print(f"  concepts   : {len(self.world_model['concepts'])}")
                print(f"  relations  : {sum(len(v) for v in self.world_model['relations'].values())}")

            except Exception as e:
                print("[V8 WORLD MODEL ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V8 STATUS]")
            print(f"  events    : {self.event_count}")
            print(f"  concepts  : {len(self.world_model['concepts'])}")
            print(f"  beliefs   : {len(self.world_model['beliefs'])}")
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
🧠 SWARM BUS V8 — SEMANTIC WORLD MODEL
========================================
✔ EVENT → CONCEPT TRANSFORMATION
✔ INTENT CLASSIFICATION
✔ WORLD STATE SIMULATION
✔ BELIEF MEMORY LAYER
✔ RELATION INFERENCE GRAPH
✔ CRDT SAFE STORAGE
========================================
""")

    bus = SwarmBusV8()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V8] SHUTDOWN")
        bus.stop()
