import socket
import threading
import json
import time

class SwarmBusV99:
    def __init__(self, port=6020):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.subscribers = []
        self.running = True

        print(f"[V9.9 BUS] ONLINE | port={self.port}")

    # --- EVENT EMITTER ---
    def emit(self, event):
        data = json.dumps(event).encode()

        # broadcast locally (swarm simulation layer)
        for sub in self.subscribers:
            try:
                sub.send(data)
            except:
                pass

    # --- EVENT LISTENER LOOP ---
    def listen(self):
        while self.running:
            data, addr = self.sock.recvfrom(4096)

            try:
                event = json.loads(data.decode())
            except:
                continue

            print(f"[BUS RX] {event}")

            # immediate re-broadcast (event-driven propagation)
            self.emit(event)

    # --- START BUS ---
    def start(self):
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

        # heartbeat event stream
        while self.running:
            self.emit({
                "type": "heartbeat",
                "node": "bus_core",
                "timestamp": time.time()
            })
            time.sleep(2)

if __name__ == "__main__":
    SwarmBusV99().start()
