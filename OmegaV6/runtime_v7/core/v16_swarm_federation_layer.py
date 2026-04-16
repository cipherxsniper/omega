import socket
import json
import time
import threading
import uuid

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


class SwarmFederationV16:
    """
    V16 Swarm Federation Layer

    Enables:
    - multi-swarm communication
    - public key exchange between swarms
    - federated trust graph
    """

    def __init__(self, port=9016):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        # identity
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

        self.node_id = str(uuid.uuid4())[:12]

        # federation maps
        self.federated_swarms = {}   # swarm_id -> public key
        self.known_nodes = {}        # node_id -> pubkey

        self.trust = {}

        self.running = True

        print(f"[V16 FEDERATION] ONLINE | node={self.node_id} | port={self.port}")

    # -----------------------------
    # SIGN
    # -----------------------------
    def sign(self, data: dict):
        raw = json.dumps(data, sort_keys=True).encode()
        return self.private_key.sign(raw).hex()

    # -----------------------------
    # VERIFY
    # -----------------------------
    def verify(self, event: dict):
        try:
            pub = event.get("pubkey")
            sig = event.get("sig")

            if not pub or not sig:
                return False

            key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub))

            raw_event = dict(event)
            del raw_event["sig"]

            raw = json.dumps(raw_event, sort_keys=True).encode()

            key.verify(bytes.fromhex(sig), raw)

            return True

        except Exception:
            return False

    # -----------------------------
    # FEDERATION HANDSHAKE
    # -----------------------------
    def handshake(self, target_ip, target_port):
        packet = {
            "type": "federation_hello",
            "node_id": self.node_id,
            "swarm_id": "V16_LOCAL_SWARM",
            "pubkey": self.public_key.public_bytes_raw().hex(),
            "timestamp": time.time()
        }

        packet["sig"] = self.sign(packet)

        self.sock.sendto(json.dumps(packet).encode(), (target_ip, target_port))

        print(f"[V16 HANDSHAKE] sent to {target_ip}:{target_port}")

    # -----------------------------
    # RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                print(f"[V16 RX] {event}")

                if not self.verify(event):
                    print("[V16 REJECTED] invalid signature")
                    continue

                self.route(event, addr)

            except Exception as e:
                print(f"[V16 ERROR] {e}")

    # -----------------------------
    # ROUTER
    # -----------------------------
    def route(self, event, addr):
        etype = event.get("type")

        if etype == "federation_hello":
            self.handle_federation(event, addr)

        elif etype == "heartbeat":
            self.handle_heartbeat(event)

        else:
            self.handle_generic(event)

    # -----------------------------
    # FEDERATION REGISTRATION
    # -----------------------------
    def handle_federation(self, event, addr):
        swarm_id = event.get("swarm_id")
        pub = event.get("pubkey")

        self.federated_swarms[swarm_id] = pub

        node = event.get("node_id")

        self.known_nodes[node] = pub

        print(f"[V16 FEDERATED] swarm={swarm_id} node={node} @ {addr[0]}")

    # -----------------------------
    # HEARTBEAT
    # -----------------------------
    def handle_heartbeat(self, event):
        node = event.get("node_id")

        self.trust[node] = self.trust.get(node, 0) + 1

        print(f"[V16 HEARTBEAT] node={node} trust={self.trust[node]}")

    # -----------------------------
    # GENERIC EVENT
    # -----------------------------
    def handle_generic(self, event):
        node = event.get("node_id")

        self.trust[node] = self.trust.get(node, 0) + 0.1

        print(f"[V16 EVENT] node={node}")

    # -----------------------------
    # HEARTBEAT LOOP
    # -----------------------------
    def heartbeat(self):
        while self.running:
            event = {
                "type": "heartbeat",
                "node_id": self.node_id,
                "pubkey": self.public_key.public_bytes_raw().hex(),
                "timestamp": time.time()
            }

            event["sig"] = self.sign(event)

            self.sock.sendto(json.dumps(event).encode(), ("127.0.0.1", self.port))

            time.sleep(3)

    # -----------------------------
    # START
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V16 FEDERATION] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    SwarmFederationV16().start()
