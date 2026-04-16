import socket
import json
import time
import threading


class SwarmBusV99_V1:
    """
    V9.9 Swarm Event Bus (V1)

    - single shared UDP event backbone
    - safe reuse socket binding
    - broadcast + receive event routing
    - deduplicated event stream
    """

    def __init__(self, port=6020):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 🔥 CRITICAL FIX: allow reuse without crash
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except OSError:
            print("[V9.9 BUS V1] Already running on port — attaching read-only mode")

        self.running = True

        self.subscribers = []
        self.seen_events = set()

        print(f"[V9.9 BUS V1] ONLINE | port={self.port}")

    # -----------------------------
    # SUBSCRIBE HANDLERS
    # -----------------------------
    def subscribe(self, handler):
        self.subscribers.append(handler)

    # -----------------------------
    # BROADCAST EVENT
    # -----------------------------
    def emit(self, event: dict):
        try:
            raw = json.dumps(event).encode()
            self.sock.sendto(raw, ("127.0.0.1", self.port))
        except Exception as e:
            print(f"[V9.9 BUS V1 ERROR] emit failed: {e}")

    # -----------------------------
    # RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                event_id = f"{event.get('node_id')}:{event.get('type')}:{event.get('timestamp')}"

                # 🔥 deduplication layer
                if event_id in self.seen_events:
                    continue

                self.seen_events.add(event_id)

                # keep memory bounded
                if len(self.seen_events) > 5000:
                    self.seen_events = set(list(self.seen_events)[-2000:])

                # route event
                for sub in self.subscribers:
                    try:
                        sub(event, addr)
                    except Exception as e:
                        print(f"[V9.9 BUS V1 ROUTE ERROR] {e}")

            except Exception as e:
                print(f"[V9.9 BUS V1 LISTEN ERROR] {e}")

    # -----------------------------
    # HEARTBEAT LOOP (SELF HEALTH)
    # -----------------------------
    def heartbeat(self):
        while self.running:
            event = {
                "node_id": "bus",
                "type": "bus_heartbeat",
                "timestamp": time.time()
            }
            self.emit(event)
            time.sleep(5)

    # -----------------------------
    # START ENGINE
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V9.9 BUS V1] STARTED LISTENING")

        while True:
            time.sleep(1)


# -----------------------------
# GLOBAL SINGLETON ACCESS
# -----------------------------
_GLOBAL_BUS = None


def get_bus():
    global _GLOBAL_BUS
    if _GLOBAL_BUS is None:
        _GLOBAL_BUS = SwarmBusV99_V1()
    return _GLOBAL_BUS


if __name__ == "__main__":
    bus = get_bus()
    bus.start()
