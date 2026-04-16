import socket
import json
import time
import threading

from runtime_v7.core.omega_memory_graph_v3 import get_memory


class SwarmBusV99_V3:
    def __init__(self, port=6020):
        self.port = port
        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except OSError:
            print("[V9.9 BUS V3] Already running — attaching")

        print(f"[V9.9 BUS V3] ONLINE | port={self.port}")

    # -----------------------------
    # EMIT EVENT
    # -----------------------------
    def emit(self, event):
        try:
            raw = json.dumps(event).encode()
            self.sock.sendto(raw, ("127.0.0.1", self.port))
        except Exception as e:
            print("[BUS EMIT ERROR]", e)

    # -----------------------------
    # LISTEN LOOP (🔥 FIXED)
    # -----------------------------
    def listen(self):
        mem = get_memory()

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                event = json.loads(data.decode())
                print(f"[V9.9 EVENT] {event}")

                # 🧠 STORE INTO MEMORY
                mem.store(event)

            except Exception as e:
                print(f"[BUS ERROR] {e}")

    # -----------------------------
    # HEARTBEAT
    # -----------------------------
    def heartbeat(self):
        while self.running:
            self.emit({
                "node_id": "bus_v3",
                "type": "bus_heartbeat",
                "timestamp": time.time()
            })
            time.sleep(5)

    # -----------------------------
    # START
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V9.9 BUS V3] STARTED")

        while True:
            time.sleep(1)


# -----------------------------
# SINGLETON
# -----------------------------
_GLOBAL = None


def get_bus():
    global _GLOBAL
    if _GLOBAL is None:
        _GLOBAL = SwarmBusV99_V3()
    return _GLOBAL


if __name__ == "__main__":
    get_bus().start()
