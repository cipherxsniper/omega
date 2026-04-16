import time
import threading
import hashlib
import hmac
import json
import socket

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaOSV4:

    def __init__(self):
        print("\n🌍 [OMEGA OS V4] BOOTING DISTRIBUTED COGNITION MESH...\n")

        # -----------------------------
        # CORE SYSTEMS
        # -----------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -----------------------------
        # NODE IDENTITY
        # -----------------------------
        self.node_id = self.generate_id()
        self.secret = b"omega-v4-secure-key"

        # -----------------------------
        # TRUST SYSTEM
        # -----------------------------
        self.trust_scores = {}

        # -----------------------------
        # NETWORK LAYER
        # -----------------------------
        self.peers = ["127.0.0.1:6100"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 6100))

        self.running = True
        self.last_index = 0

        # -----------------------------
        # START SYSTEM THREADS
        # -----------------------------
        threading.Thread(target=self.listen_loop, daemon=True).start()
        threading.Thread(target=self.cognition_loop, daemon=True).start()

        print(f"\n🌍 [OMEGA OS V4] ONLINE | node={self.node_id}\n")

    # -----------------------------
    # NODE IDENTITY
    # -----------------------------
    def generate_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

    def verify(self, event, signature):
        return hmac.compare_digest(self.sign(event), signature)

    # -----------------------------
    # NETWORK LISTENER
    # -----------------------------
    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                sig = event.get("signature")
                if not sig:
                    continue

                if not self.verify(event, sig):
                    continue

                self.memory.apply(event)

            except Exception:
                pass

    # -----------------------------
    # BROADCAST
    # -----------------------------
    def broadcast(self, event):
        raw = json.dumps(event).encode()

        for peer in self.peers:
            try:
                ip, port = peer.split(":")
                self.sock.sendto(raw, (ip, int(port)))
            except Exception:
                pass

    # -----------------------------
    # COGNITION ENGINE (SEMANTIC)
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state["events"]
                new_events = events[self.last_index:]
                self.last_index = len(events)

                for e in new_events:
                    meaning = self.semantic.interpret(e)

                    # 🧠 convert raw event → structured meaning
                    node = {
                        "entity": meaning.get("entity", "unknown"),
                        "relation": meaning.get("relation", "observed"),
                        "confidence": meaning.get("confidence", 0.5)
                    }

                    print(f"[V4 MEANING] {node}")

                time.sleep(1)

            except Exception as e:
                print("[V4 COGNITION ERROR]", e)

    # -----------------------------
    # EMIT EVENT (SIGNED + SYNC)
    # -----------------------------
    def emit(self, event):
        event["node_id"] = self.node_id
        event["timestamp"] = time.time()
        event["signature"] = self.sign(event)

        self.memory.apply(event)
        self.broadcast(event)

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

            print(f"[OMEGA V4] {user}")


if __name__ == "__main__":
    OmegaOSV4().run()
