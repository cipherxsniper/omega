# OMEGA EVENT ROUTER v2 (DISTRIBUTED)
# Lightweight TCP message bus

import json
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5055


class EventRouterV2:
    def __init__(self):
        self.subscribers = []

    def emit(self, event_type, payload=None):
        event = {
            "type": event_type,
            "payload": payload,
            "ts": str(datetime.utcnow())
        }

        msg = json.dumps(event).encode()

        for port in self.subscribers:
            try:
                with socket.socket() as s:
                    s.connect((HOST, port))
                    s.sendall(msg)
            except:
                pass

    def subscribe(self, port):
        self.subscribers.append(port)


def start_listener(port, handler):
    def run():
        with socket.socket() as s:
            s.bind((HOST, port))
            s.listen()

            print(f"[Ω BUS v2] listening on {port}")

            while True:
                conn, _ = s.accept()
                data = conn.recv(65536)

                try:
                    event = json.loads(data.decode())
                    handler(event)
                except:
                    pass

    t = threading.Thread(target=run, daemon=True)
    t.start()


ROUTER = EventRouterV2()
