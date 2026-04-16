import time
import json
import socket

class SwarmTransportV771:
    def __init__(self, port=6001):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Termux-safe mode (no raw broadcast permission issues)
        self.targets = ["127.0.0.1"]

    def send_lan(self, msg, target):
        try:
            data = json.dumps(msg).encode()
            self.sock.sendto(data, ("127.0.0.1", self.port))
        except Exception as e:
            print("[LAN SEND ERROR]", e)

    def send_relay(self, msg, target):
        try:
            data = json.dumps(msg).encode()
            self.sock.sendto(data, ("127.0.0.1", self.port))
        except Exception as e:
            print("[RELAY SEND ERROR]", e)

    def recv_loop(self, handler):
        self.sock.bind(("0.0.0.0", self.port))

        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())
                handler(msg, addr)
            except Exception:
                pass
