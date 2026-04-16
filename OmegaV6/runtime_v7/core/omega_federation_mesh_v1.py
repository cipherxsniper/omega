import socket
import json
import threading
from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class FederationMeshV1:

    def __init__(self, port=6100):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.crdt = get_crdt()

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except:
            print("[FEDERATION] Already running")

        print(f"[FEDERATION V1] ONLINE | port={self.port}")

        threading.Thread(target=self.listen, daemon=True).start()

    # -------------------------
    # BROADCAST EVENT
    # -------------------------
    def broadcast(self, event):
        raw = json.dumps(event).encode()
        self.sock.sendto(raw, ("127.0.0.1", self.port))

    # -------------------------
    # LISTEN
    # -------------------------
    def listen(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                self.crdt.apply(event)

                print(f"[FEDERATION EVENT] {event.get('type')}")

            except Exception as e:
                print("[FEDERATION ERROR]", e)
