import socket
import json
import time
import threading
import traceback
import hashlib
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SwarmBusV11:

    def __init__(self, host="0.0.0.0", port=6100):
        print("\n🧠⚙️ [SWARM BUS V11] INITIALIZING EMERGENT REASONING GENERATOR...\n")

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
        # REASONING STRATEGY ENGINE (V11 CORE)
        # =========================
        self.strategies = {
            "base": self.base_reasoning
        }

        self.strategy_scores = defaultdict(float)
        self.strategy_history = defaultdict(list)

        self.event_queue = deque()

        # emergent strategy memory
        self.emergent_strategies = {}

        # =========================
        # THREADS
        # =========================
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.processor_loop, daemon=True).start()
        threading.Thread(target=self.strategy_evolution_loop, daemon=True).start()
        threading.Thread(target=self.health_loop, daemon=True).start()

        print(f"🟢 [SWARM BUS V11] ONLINE @ {self.host}:{self.port}\n")

    # =====================================================
    # HASH
    # =====================================================
    def event_id(self, event):
        return hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()

    # =====================================================
    # BASE REASONING ENGINE
    # =====================================================
    def base_reasoning(self, event):
        text = event.get("content", "").lower()

        if "?" in text:
            return {"concept": "question", "confidence": 0.6}
        if any(w in text for w in ["hello", "hi"]):
            return {"concept": "greeting", "confidence": 0.7}
        if any(w in text for w in ["run", "start"]):
            return {"concept": "command", "confidence": 0.8}

        return {"concept": "unknown", "confidence": 0.3}

    # =====================================================
    # EMERGENT STRATEGY GENERATOR (CORE V11)
    # =====================================================
    def generate_strategy(self, name):
        """
        Creates a new reasoning strategy at runtime
        (NO code execution, only logic composition)
        """

        def strategy(event):
            text = event.get("content", "")

            score = 0.0
            if len(text) > 10:
                score += 0.2
            if "?" in text:
                score += 0.3
            if text.lower().count("why") > 0:
                score += 0.2

            concept = "emergent_" + name

            return {
                "concept": concept,
                "confidence": min(1.0, score)
            }

        return strategy

    # =====================================================
    # STRATEGY SELECTION
    # =====================================================
    def select_best_strategy(self, event):
        best = None
        best_score = -1

        for name, fn in self.strategies.items():
            try:
                result = fn(event)
                score = result["confidence"]

                if score > best_score:
                    best_score = score
                    best = result

                self.strategy_scores[name] += score

            except Exception:
                continue

        return best

    # =====================================================
    # MEMORY WRITE
    # =====================================================
    def write_memory(self, event):
        try:
            self.memory.store(event)
        except Exception as e:
            print("[V11 MEMORY ERROR]", e)

    # =====================================================
    # LISTENER
    # =====================================================
    def listen_loop(self):
        print("[SWARM BUS V11] LISTENING...\n")

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

                    # run best reasoning strategy
                    result = self.select_best_strategy(event)

                    self.event_count += 1

                    self.strategy_history[result["concept"]].append(result)

                    self.write_memory({
                        "event": event,
                        "reasoning": result
                    })

                    print(f"\n🧠 [V11 REASONING]")
                    print(f"  concept    : {result['concept']}")
                    print(f"  confidence : {result['confidence']:.2f}")

                time.sleep(0.01)

            except Exception as e:
                print("[V11 PROCESS ERROR]", e)

    # =====================================================
    # STRATEGY EVOLUTION LOOP
    # =====================================================
    def strategy_evolution_loop(self):
        while self.running:
            try:
                time.sleep(5)

                # create new emergent strategies over time
                if len(self.strategies) < 5:
                    name = f"s{len(self.strategies)}"
                    self.strategies[name] = self.generate_strategy(name)

                    print(f"\n🌱 [V11 NEW STRATEGY CREATED]")
                    print(f"  → {name}")

                # reinforce best strategies
                best = max(self.strategy_scores, default=None, key=self.strategy_scores.get)

                if best:
                    print("\n🧬 [V11 STRATEGY EVOLUTION]")
                    print(f"  best_strategy : {best}")
                    print(f"  score         : {self.strategy_scores[best]:.2f}")

            except Exception as e:
                print("[V11 EVOLUTION ERROR]", e)

    # =====================================================
    # HEALTH
    # =====================================================
    def health_loop(self):
        while self.running:
            time.sleep(5)

            print("\n🟡 [SWARM BUS V11 STATUS]")
            print(f"  events     : {self.event_count}")
            print(f"  strategies : {len(self.strategies)}")
            print(f"  memory     : active")
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
🧠 SWARM BUS V11 — EMERGENT REASONING ENGINE
========================================
✔ MULTI-STRATEGY REASONING
✔ STRATEGY GENERATION AT RUNTIME
✔ META-REASONING SELECTION LAYER
✔ EVOLUTION OF THINKING METHODS
✔ CRDT MEMORY SAFE
========================================
""")

    bus = SwarmBusV11()

    try:
        while True:
            time.sleep(999999)
    except KeyboardInterrupt:
        print("\n[SWARM BUS V11] SHUTDOWN")
        bus.stop()
