import socket
import json
import time
import threading
import uuid

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)


class CryptoSwarmIdentityV15:
    """
    V15 Cryptographic Swarm Identity Layer

    Adds:
    - node identity keys
    - signed events
    - verification pipeline
    - trust scoring
    """

    def __init__(self, port=8015):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        # identity keys
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        self.node_id = str(uuid.uuid4())[:12]

        # known nodes: node_id -> public_key
        self.known_keys = {}

        # trust scoring
        self.trust_score = {}

        self.running = True

        print(f"[V15 IDENTITY] ONLINE | node={self.node_id} | port={self.port}")

    # -----------------------------
    # SIGN EVENT
    # -----------------------------
    def _sign(self, event: dict):
        raw = json.dumps(event, sort_keys=True).encode()
        return self.private_key.sign(raw).hex()

    # -----------------------------
    # VERIFY EVENT
    # -----------------------------
    def _verify(self, event: dict):
        node_id = event.get("node_id")
        sig = event.get("sig")
        pub = event.get("pubkey")

        if not node_id or not sig or not pub:
            return False

        try:
            pub_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub))

            raw_event = dict(event)
            del raw_event["sig"]

            raw = json.dumps(raw_event, sort_keys=True).encode()

            pub_key.verify(bytes.fromhex(sig), raw)

            self.known_keys[node_id] = pub_key

            return True

        except Exception:
            return False

    # -----------------------------
    # SEND EVENT
    # -----------------------------
    def send(self, event):
        event["node_id"] = self.node_id
        event["pubkey"] = self.public_key.public_bytes_raw().hex()
        event["sig"] = self._sign(event)

        self.sock.sendto(json.dumps(event).encode(), ("127.0.0.1", self.port))

    # -----------------------------
    # RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                print(f"[V15 RX] {event}")

                if self._verify(event):
                    self._accept(event)
                else:
                    self._reject(event)

            except Exception as e:
                print(f"[V15 ERROR] {e}")

    # -----------------------------
    # ACCEPT VALID EVENT
    # -----------------------------
    def _accept(self, event):
        node = event["node_id"]

        self.trust_score[node] = self.trust_score.get(node, 0) + 1

        print(f"[V15 ACCEPTED] node={node} trust={self.trust_score[node]}")

    # -----------------------------
    # REJECT INVALID EVENT
    # -----------------------------
    def _reject(self, event):
        node = event.get("node_id", "unknown")

        self.trust_score[node] = self.trust_score.get(node, 0) - 1

        print(f"[V15 REJECTED] node={node}")

    # -----------------------------
    # HEARTBEAT LOOP
    # -----------------------------
    def heartbeat(self):
        while self.running:
            self.send({
                "type": "heartbeat",
                "timestamp": time.time()
            })
            time.sleep(3)

    # -----------------------------
    # START
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V15 IDENTITY] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    CryptoSwarmIdentityV15().start()
