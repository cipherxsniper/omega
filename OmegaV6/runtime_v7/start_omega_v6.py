import time
import threading
import hashlib
import hmac
import json
import socket

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV6:

    def __init__(self):
        print("\n🧠🌍 [OMEGA OS V6] BOOTING WORLD SIMULATION ENGINE...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v6-simulation-key"

        # -----------------------------
        # TRUST ECONOMY
        # -----------------------------
        self.trust = {}
        self.prediction_score = {}

        # -----------------------------
        # WORLD MODEL (SIMULATION CORE)
        # -----------------------------
        self.world_model = {
            "entities": {},
            "relations": {},
            "probabilities": {}
        }

        # -----------------------------
        # WAN MESH
        # -----------------------------
        self.peers = ["127.0.0.1:6100"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 6100))

        self.running = True
        self.last_index = 0

        # -----------------------------
        # THREADS
        # -----------------------------
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.cognition_loop, daemon=True).start()
        threading.Thread(target=self.simulation_loop, daemon=True).start()

        print(f"\n🧠 [OMEGA OS V6] ONLINE | node={self.node_id}\n")

    # -----------------------------
    # IDENTITY
    # -----------------------------
    def generate_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

    def verify(self, event, signature):
        return hmac.compare_digest(self.sign(event), signature)

    # -----------------------------
    # WORLD MODEL UPDATE
    # -----------------------------
    def update_world_model(self, meaning):
        entity = meaning.get("entity", "unknown")

        if entity not in self.world_model["entities"]:
            self.world_model["entities"][entity] = {"count": 0}

        self.world_model["entities"][entity]["count"] += 1

        # probability drift simulation
        self.world_model["probabilities"][entity] = min(
            1.0,
            self.world_model["entities"][entity]["count"] * 0.01
        )

    # -----------------------------
    # SIMULATION LOOP (NEW CORE)
    # -----------------------------
    def simulation_loop(self):
        while self.running:
            try:
                for entity, data in self.world_model["entities"].items():
                    prob = self.world_model["probabilities"].get(entity, 0.0)

                    prediction = {
                        "entity": entity,
                        "next_likelihood": prob,
                        "state": "simulated_future"
                    }

                    print(f"[V6 SIMULATION] {prediction}")

                time.sleep(3)

            except Exception as e:
                print("[V6 SIM ERROR]", e)

    # -----------------------------
    # NETWORK LISTENER
    # -----------------------------
    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                if not self.verify(event, event.get("signature")):
                    continue

                self.memory.apply(event)

            except Exception:
                pass

    # -----------------------------
    # COGNITION LOOP
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:
                    meaning = self.semantic.interpret(e)

                    self.update_world_model(meaning)

                    print(f"[V6 MEANING] {meaning}")

                time.sleep(1)

            except Exception as e:
                print("[V6 COGNITION ERROR]", e)

    # -----------------------------
    # EMIT EVENT
    # -----------------------------
    def emit(self, event):
        event["node_id"] = self.node_id
        event["timestamp"] = time.time()
        event["signature"] = self.sign(event)

        self.memory.apply(event)

    # -----------------------------
    # CLI
    # -----------------------------
    def run(self):
        while True:
            user = input("\n~Omega$> ").strip()

            if user.lower() == "exit":
                break

            self.emit({
                "type": "user_input",
                "content": user
            })

            print(f"[OMEGA V6] {user}")


if __name__ == "__main__":
    OmegaOSV6().run()
