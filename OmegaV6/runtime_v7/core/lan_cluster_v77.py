import socket
import json
import time
import threading
import hashlib

class SafeLANClusterV77:
    def __init__(self, port=7001):
        self.port = port
        self.peers = {}
        self.running = True

        self.node_id = hashlib.sha256(str(time.time()).encode()).hexdigest()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

    def scan_lan(self):
        base_ips = [
            "192.168.0.",
            "192.168.1.",
            "10.0.0."
        ]

        discovered = []

        for base in base_ips:
            for i in range(1, 255):
                ip = f"{base}{i}"
                try:
                    test = socket.socket()
                    test.settimeout(0.05)
                    test.connect((ip, self.port))
                    discovered.append(ip)
                    test.close()
                except:
                    pass

        return discovered

    def send_handshake(self, ip):
        payload = {
            "node_id": self.node_id,
            "type": "v7_7_handshake",
            "timestamp": time.time()
        }

        self.sock.sendto(json.dumps(payload).encode(), (ip, self.port))

    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())

                node_id = msg.get("node_id")

                if node_id:
                    self.peers[node_id] = time.time()

                print("[V7.7 SAFE RX]", msg)

            except:
                pass

    def run(self):
        threading.Thread(target=self.listen, daemon=True).start()

        while self.running:
            targets = self.scan_lan()

            for ip in targets:
                self.send_handshake(ip)

            time.sleep(5)
