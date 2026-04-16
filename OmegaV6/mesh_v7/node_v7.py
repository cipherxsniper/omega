import json
import time
from net.cognitive_bus import CognitiveBusV7


class OmegaNodeV7:

    def __init__(self, node_id, engine, port):
        self.node_id = node_id
        self.engine = engine
        self.port = port
        self.bus = CognitiveBusV7(port=port)

    def handle_connection(self, conn, addr):
        data = conn.recv(65535)
        try:
            frame = json.loads(data.decode())
            print(f"[{self.node_id}] received frame from network")
        except:
            pass
        conn.close()

    def start(self):
        import threading
        threading.Thread(target=self.bus.start_server, args=(self.handle_connection,)).start()

    def step(self):
        frame = self.engine.step()

        frame["node_id"] = self.node_id
        frame["timestamp"] = time.time()

        return frame
