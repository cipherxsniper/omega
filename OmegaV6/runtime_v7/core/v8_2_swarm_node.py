import socket
import threading
import time
import json
import uuid
import hashlib


# -------------------------
# NODE IDENTITY
# -------------------------
def generate_node_id():
    raw = f"{uuid.uuid4()}:{time.time()}"
    return hashlib.sha256(raw.encode()).hexdigest()


class SwarmNodeV82:
    def __init__(self, port, peer_ports):
        self.node_id = generate_node_id()
        self.port = port
        self.peer_ports = peer_ports

        self.peers = {}
        self.memory = []

        # UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.running = True

    # -------------------------
    # SEND MESSAGE
    # -------------------------
    def send(self, msg, port):
        try:
            data = json.dumps(msg).encode()
            self.sock.sendto(data, ("127.0.0.1", port))
        except Exception as e:
            print("[SEND ERROR]", e)

    # -------------------------
    # BROADCAST TO PEERS
    # -------------------------
    def broadcast(self):
        while self.running:
            payload = {
                "node_id": self.node_id,
                "memory_size": len(self.memory),
                "timestamp": time.time()
            }

            for p in self.peer_ports:
                self.send(payload, p)

            time.sleep(2)

    # -------------------------
    # LISTEN LOOP
    # -------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                msg = json.loads(data.decode())

                sender = msg.get("node_id")

                if sender and sender != self.node_id:
                    self.peers[sender] = time.time()

                self.memory.append(msg)

                print(f"[NODE {self.port}] RX:", msg)

            except Exception:
                pass

    # -------------------------
    # START NODE
    # -------------------------
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.broadcast, daemon=True).start()

        print(f"[V8.2 NODE STARTED] port={self.port} id={self.node_id}")
