import socket
import json
import time
import threading
import uuid


class V17LanAutoEnrollmentSwarm:

    def __init__(self, port=6017):
        self.port = port
        self.node_id = str(uuid.uuid4())[:12]

        self.peers = {}          # node_id -> ip
        self.trusted = set()     # trusted nodes
        self.seen = set()        # dedup protection

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.running = True

        print(f"[V17] SWARM ONLINE | node={self.node_id} | port={self.port}")

    # ----------------------------
    # RECEIVE LOOP
    # ----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                msg = json.loads(data.decode())

                node_id = msg.get("node_id")
                msg_type = msg.get("type")

                if not node_id:
                    continue

                # 🔥 DEDUP CORE (FIXES YOUR LOOP BUG)
                key = f"{node_id}:{addr[0]}"

                if key in self.seen:
                    continue

                self.seen.add(key)

                # ----------------------------
                # ENROLLMENT FLOW
                # ----------------------------
                if msg_type == "hello":
                    self.handle_hello(node_id, addr)

                elif msg_type == "heartbeat":
                    self.handle_heartbeat(node_id, addr)

                elif msg_type == "ack":
                    self.handle_ack(node_id, addr)

            except Exception as e:
                print(f"[V17 ERROR] {e}")

    # ----------------------------
    # HELLO (DISCOVERY)
    # ----------------------------
    def handle_hello(self, node_id, addr):
        self.peers[node_id] = addr[0]

        print(f"[V17 DISCOVERY] peer={node_id} @ {addr[0]}")

        # auto-ack enrollment
        self.send_ack(node_id, addr[0])

    # ----------------------------
    # HEARTBEAT
    # ----------------------------
    def handle_heartbeat(self, node_id, addr):
        self.peers[node_id] = addr[0]

        print(f"[V17 HEARTBEAT] {node_id} @ {addr[0]}")

        if node_id not in self.trusted:
            self.trusted.add(node_id)
            print(f"[V17 TRUSTED] {node_id}")

    # ----------------------------
    # ACK
    # ----------------------------
    def handle_ack(self, node_id, addr):
        if node_id not in self.trusted:
            self.trusted.add(node_id)

        print(f"[V17 ACK RECEIVED] {node_id} @ {addr[0]}")

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
            print(f"[V17 STATUS] peers={len(self.peers)} trusted={len(self.trusted)}")
            time.sleep(5)

    # ----------------------------
    # START
    # ----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.status_loop, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(1)


if __name__ == "__main__":
    V17LanAutoEnrollmentSwarm().start()

