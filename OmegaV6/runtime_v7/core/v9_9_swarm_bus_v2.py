from runtime_v7.core.omega_memory_graph_v2 import get_memory
import socket
import json
import time
import threading


class SwarmBusV99_V2:
    """
    V9.9 Swarm Event Bus (V2)
    - stable shared UDP event spine
    - deduplication
    - live event visibility
    """

    def __init__(self, port=6020):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # allow reuse without crash
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except OSError:
            print("[V9.9 BUS V2] Already running — attaching read-only mode")

        self.running = True
        self.subscribers = []
        self.seen_events = set()

        print(f"[V9.9 BUS V2] ONLINE | port={self.port}")

    # -----------------------------
    # SUBSCRIBE
    # -----------------------------
    def subscribe(self, handler):
        self.subscribers.append(handler)

    # -----------------------------
    # EMIT EVENT
    # -----------------------------
    def emit(self, event: dict):
        try:
            raw = json.dumps(event).encode()
            self.sock.sendto(raw, ("127.0.0.1", self.port))
        except Exception as e:
            print(f"[V9.9 BUS V2 ERROR] emit failed: {e}")

    # -----------------------------
    # LISTENER LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                # parse event first (live visibility)
                event = json.loads(data.decode())
                print(f"[V9.9 EVENT] {event}")

                event_id = f"{event.get('node_id')}:{event.get('type')}:{event.get('timestamp')}"

                # dedup protection
                if event_id in self.seen_events:
                    continue

                self.seen_events.add(event_id)

                if len(self.seen_events) > 5000:
                    self.seen_events = set(list(self.seen_events)[-2000:])

                # route event
                for sub in self.subscribers:
                    try:
                        sub(event, addr)
                    except Exception as e:
                        print(f"[V9.9 ROUTE ERROR] {e}")

            except Exception as e:
                print(f"[V9.9 LISTEN ERROR] {e}")

    # -----------------------------
    # HEARTBEAT
    # -----------------------------
    def heartbeat(self):
        while self.running:
            self.emit({
                "node_id": "bus",
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

        print("[V9.9 BUS V2] STARTED")

        while True:
            time.sleep(1)


# -----------------------------
# SINGLETON ACCESS
# -----------------------------
_GLOBAL_BUS = None


def get_bus():
    global _GLOBAL_BUS
    if _GLOBAL_BUS is None:
        _GLOBAL_BUS = SwarmBusV99_V2()
    return _GLOBAL_BUS


if __name__ == "__main__":
    get_bus().start()

# === OMEGA V2 MEMORY HOOK ===
from runtime_v7.core.omega_memory_graph_v2 import get_memory

# === OMEGA MEMORY INGEST PATCH (INSERT INTO listen loop AFTER JSON PARSE) ===
# Replace:
# event = json.loads(data.decode())
#
# WITH:
# event = json.loads(data.decode())
# get_memory().ingest(event)
# print(f"[V9.9 EVENT] {event}")

# === AUTO MEMORY INTEGRATION SAFETY PATCH ===
try:
    from runtime_v7.core.omega_memory_graph_v2 import get_memory
    MEMORY = get_memory()
except Exception as e:
    print("[V9.9 MEMORY HOOK FAILED]", e)
    MEMORY = None

# === FORCE MEMORY INGEST (SAFE GUARD) ===
if MEMORY:
    MEMORY.ingest(event)
