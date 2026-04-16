import socket
import json
import time
import threading
import uuid


class V17LanAutoEnrollmentSwarmV2:

    def __init__(self, port=6017):
        self.port = port
        self.node_id = str(uuid.uuid4())[:12]

        self.peers = {}       # node_id -> ip
        self.trusted = set()  # trusted nodes
        self.seen = set()     # dedup guard

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.running = True

        print(f"[V17-V2] SWARM ONLINE | node={self.node_id} | port={self.port}")

    # ----------------------------
    # LISTENER LOOP (HARDENED)
    # ----------------------------
    def listen(self):
        print("[V17-V2] LISTENER BOOTED")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                msg = json.loads(data.decode())

                node_id = msg.get("node_id")
                msg_type = msg.get("type")

                if not node_id:
                    continue

                key = f"{node_id}:{addr[0]}"

                if key in self.seen:
                    continue

                self.seen.add(key)

                print(f"[V17-V2 RX] {msg_type} from {node_id} @ {addr[0]}")

                if msg_type == "hello":
                    self.handle_hello(node_id, addr)

                elif msg_type == "heartbeat":
                    self.handle_heartbeat(node_id, addr)

                elif msg_type == "ack":
                    self.handle_ack(node_id, addr)

            except Exception as e:
                print(f"[V17-V2 ERROR] listener crash: {e}")

    # ----------------------------
    # HELLO (DISCOVERY)
    # ----------------------------
    def handle_hello(self, node_id, addr):
        self.peers[node_id] = addr[0]

        print(f"[V17-V2 DISCOVERY] peer={node_id} @ {addr[0]}")

        self.send_ack(node_id, addr[0])

    # ----------------------------
    # HEARTBEAT
    # ----------------------------
    def handle_heartbeat(self, node_id, addr):
        self.peers[node_id] = addr[0]

        print(f"[V17-V2 HEARTBEAT] {node_id} @ {addr[0]}")

        if node_id not in self.trusted:
            self.trusted.add(node_id)
            print(f"[V17-V2 TRUSTED] {node_id}")

    # ----------------------------
    # ACK
    # ----------------------------
    def handle_ack(self, node_id, addr):
        if node_id not in self.trusted:
            self.trusted.add(node_id)

        print(f"[V17-V2 ACK RECEIVED] {node_id} @ {addr[0]}")

    # ----------------------------
    # SEND ACK
    # ----------------------------
    def send_ack(self, node_id, ip):
        payload = {
            "node_id": self.node_id,
            "type": "ack",
            "target": node_id,
            "timestamp": time.time()
        }

        self.sock.sendto(json.dumps(payload).encode(), (ip, self.port))

    # ----------------------------
    # STATUS LOOP
    # ----------------------------
    def status_loop(self):
        while self.running:
            print(
                f"[V17-V2 STATUS] peers={len(self.peers)} "
                f"trusted={len(self.trusted)} seen={len(self.seen)}"
            )
            time.sleep(5)

    # ----------------------------
    # START (HARDENED LIFECYCLE)
    # ----------------------------
    def start(self):
        print("[V17-V2] STARTING SWARM ENGINE")

        listener = threading.Thread(target=self.listen, daemon=False)
        status = threading.Thread(target=self.status_loop, daemon=True)

        listener.start()
        status.start()

        print("[V17-V2] ALL THREADS ACTIVE")

        # HARD BLOCK (prevents silent death)
        listener.join()


if __name__ == "__main__":
    V17LanAutoEnrollmentSwarmV2().start()
