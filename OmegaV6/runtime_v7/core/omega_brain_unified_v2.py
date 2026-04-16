import time
import threading
import hashlib
from runtime_v7.core.omega_memory_graph_v3 import get_memory


class OmegaBrainUnifiedV2:
    """
    OMEGA V2:
    - Recursive Self Improvement
    - Federation Memory Graph
    - Trust + Identity Layer
    """

    def __init__(self):
        self.memory = get_memory()

        self.running = True
        self.last_index = 0

        self.thought_buffer = []

        # -----------------------------
        # FEDERATION STATE
        # -----------------------------
        self.node_id = self.generate_node_id()
        self.trust_db = {}  # node_id -> trust score

        # -----------------------------
        # SELF-IMPROVEMENT RULES
        # -----------------------------
        self.reasoning_rules = {
            "heartbeat": "observe",
            "ping": "verify_network",
            "unknown": "analyze"
        }

        print(f"[OMEGA V2] ONLINE | node={self.node_id}")
        print("[FEDERATION + SELF-IMPROVEMENT + TRUST ACTIVE]")

        self.lock = threading.Lock()

        # background loops
        threading.Thread(target=self.cognition_loop, daemon=True).start()
        threading.Thread(target=self.self_improve_loop, daemon=True).start()

    # -----------------------------
    # NODE IDENTITY
    # -----------------------------
    def generate_node_id(self):
        raw = str(time.time()).encode()
        return hashlib.sha256(raw).hexdigest()[:12]

    def sign_event(self, event: dict):
        payload = str(event).encode()
        return hashlib.sha256(payload + self.node_id.encode()).hexdigest()

    # -----------------------------
    # TRUST SYSTEM
    # -----------------------------
    def update_trust(self, node_id, delta):
        if node_id not in self.trust_db:
            self.trust_db[node_id] = 1.0

        self.trust_db[node_id] += delta

        # clamp
        self.trust_db[node_id] = max(0.0, min(10.0, self.trust_db[node_id]))

    def is_trusted(self, node_id):
        return self.trust_db.get(node_id, 1.0) > 0.5

    # -----------------------------
    # COGNITION LOOP
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.memory.get("events", [])
                new_events = events[self.last_index:]
                self.last_index = len(events)

                thoughts = []

                for e in new_events:
                    node = e.get("node_id", "unknown")
                    etype = e.get("type", "unknown")

                    # TRUST FILTER
                    if not self.is_trusted(node) and node != "unknown":
                        self.update_trust(node, -0.1)
                        continue

                    rule = self.reasoning_rules.get(etype, "analyze")

                    if rule == "observe":
                        thoughts.append("System heartbeat observed.")
                    elif rule == "verify_network":
                        thoughts.append("Network signal validated.")
                    else:
                        thoughts.append(f"Analyzing emergent pattern: {etype}")

                with self.lock:
                    self.thought_buffer = thoughts[-7:]

                time.sleep(1)

            except Exception as e:
                print("[COGNITION ERROR]", e)
                time.sleep(2)

    # -----------------------------
    # SELF-IMPROVEMENT LOOP
    # -----------------------------
    def self_improve_loop(self):
        while self.running:
            try:
                events = self.memory.memory.get("events", [])

                # adaptive rule tuning
                type_count = {}

                for e in events[-50:]:
                    t = e.get("type", "unknown")
                    type_count[t] = type_count.get(t, 0) + 1

                # if heartbeat dominates → simplify reasoning
                if type_count.get("heartbeat", 0) > 10:
                    self.reasoning_rules["heartbeat"] = "light_observe"

                # if unknown events grow → increase analysis depth
                if type_count.get("unknown", 0) > 5:
                    self.reasoning_rules["unknown"] = "deep_analyze"

                time.sleep(5)

            except Exception as e:
                print("[SELF-IMPROVE ERROR]", e)
                time.sleep(3)

    # -----------------------------
    # RESPONSE ENGINE
    # -----------------------------
    def respond(self, user_input: str):

        user_input = user_input.lower()

        if "thought" in user_input:
            with self.lock:
                return " | ".join(self.thought_buffer) if self.thought_buffer else "No active cognition yet."

        if "rules" in user_input:
            return str(self.reasoning_rules)

        if "trust" in user_input:
            return str(self.trust_db)

        events = self.memory.memory.get("events", [])

        if events:
            last = events[-1]
            return f"Federation event: {last.get('type')} | node={last.get('node_id')}"

        return "Omega V2 is listening across federation layer..."

    # -----------------------------
    # CHAT LOOP
    # -----------------------------
    def chat(self):
        while self.running:
            try:
                user = input("\n~Omega$> ")

                if user == "exit":
                    self.running = False
                    break

                print(f"Omega > {self.respond(user)}")

            except KeyboardInterrupt:
                self.running = False
                break


if __name__ == "__main__":
    OmegaBrainUnifiedV2().chat()x
