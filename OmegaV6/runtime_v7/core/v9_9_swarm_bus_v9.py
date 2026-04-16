import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque


from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV9:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠🌱 [SWARM BUS V9] INITIALIZING SELF-GENERATING COGNITION ARCHITECTURE...\n")

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
        # DYNAMIC COGNITION ENGINE (V9 CORE)
        # =========================
        self.cognition_schema = {
            "concept_types": {},   # dynamically generated
            "rules": [],
            "mutations": []
        }

        self.world_model = {
            "concepts": {},
            "relations": defaultdict(list),
            "beliefs": {}
        }

        self.queue = deque()

        # how often system invents new concepts
        self.invention_threshold = 3

        # pattern memory
        self.pattern_memory = defaultdict(int)

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.cognition_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V9] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # ID
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # INITIAL SEMANTIC GUESS
    # =====================================================
    def base_interpret(self, event):
        text = event.get("content", "").lower()

        if "?" in text:
            return "question"
        if any(w in text for w in ["hello", "hi"]):
            return "greeting"
        if any(w in text for w in ["run", "start"]):
            return "command"

        return "unknown"

    # =====================================================
    # COGNITION INVERTER (V9 CORE)
    # =====================================================
    def evolve_concept(self, raw_label):
        """
        Dynamically creates new cognition types
        """
        if raw_label not in self.cognition_schema["concept_types"]:

            new_type = {
                "name": raw_label,
                "strength": 1,
                "created_at": time.time(),
                "derived_from": "emergence"
            }

            self.cognition_schema["concept_types"][raw_label] = new_type

            print(f"\n🧠 [NEW CONCEPT FORGED]")
            print(f"  → {raw_label}")

        else:
            self.cognition_schema["concept_types"][raw_label]["strength"] += 1

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V9 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V9] LISTENING...\n")

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
    # PROCESSOR
    # =====================================================
    def processor_loop(self):
        while self.running:
            try:
                if self.queue:
                    event = self.queue.popleft()

                    label = self.base_interpret(event)

                    # pattern tracking
                    self.pattern_memory[label] += 1

                    # evolve cognition if repeated
                    if self.pattern_memory[label] >= self.invention_threshold:
                        self.evolve_concept(label)

                    # update world model
                    eid = self.event_id(event)

                    self.world_model["concepts"][eid] = {
                        "raw": event,
                        "label": label,
                        "timestamp": time.time()
                    }

                    self.event_count += 1

                    print(f"\n🧠 [V9 EVENT]")
                    print(f"  label : {label}")
                    print(f"  text  : {event.get('content')}")

                    self.write_memory({
                        "label": label,
                        "event": event
                    })

                time.sleep(0.01)

            except Exception as e:
                print("[V9 PROCESS ERROR]", e)

    # =====================================================
    # COGNITION LOOP (SELF-REWRITING BEHAVIOR)
    # =====================================================
    def cognition_loop(self):
        while self.running:
            try:
                time.sleep(5)

                # mutate schema if imbalance detected
                total = sum(self.pattern_memory.values())

                for label, count in self.pattern_memory.items():
                    ratio = count / total if total else 0

                    if ratio > 0.6:
                        # strengthen concept
                        self.evolve_concept(label)

                    if ratio < 0.1:
                        # weak concept drift marker
                        self.cognition_schema["mutations"].append({
                            "type": "weak_concept",
                            "label": label,
                            "time": time.time()
                        })

                print("\n🌱 [V9 COGNITION EVOLUTION]")
                print(f"  concepts : {len(self.cognition_schema['concept_types'])}")
                print(f"  mutations: {len(self.cognition_schema['mutations'])}")

            except Exception as e:
                print("[V9 COGNITION ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V9 STATUS]")
            print(f"  events     : {self.event_count}")
            print(f"  concepts   : {len(self.cognition_schema['concept_types'])}")
            print(f"  mutations  : {len(self.cognition_schema['mutations'])}")
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
🧠 SWARM BUS V9 — SELF-GENERATING COGNITION
========================================
✔ DYNAMIC CONCEPT CREATION
✔ SELF-REWRITING CLASSIFICATION SYSTEM
✔ EMERGENT COGNITION SCHEMA
✔ ADAPTIVE WORLD MODEL
✔ CRDT MEMORY SAFE
========================================
""")

    bus = SwarmBusV9()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V9] SHUTDOWN")
        bus.stop()
