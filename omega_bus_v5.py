import socket
import json
import threading

class OmegaBusV5:
    def __init__(self, port=5080):
        self.port = port
        self.handlers = []

    def on(self, fn):
        self.handlers.append(fn)

    def start(self):
        def run():
            s = socket.socket()
            s.bind(("0.0.0.0", self.port))
            s.listen(50)

            print(f"[Ω-BUS v5] SWARM ACTIVE on {self.port}")

            while True:
                conn, _ = s.accept()
                try:
                    msg = json.loads(conn.recv(8192).decode())
                    for h in self.handlers:
                        h(msg)
                except:
                    pass
                conn.close()

        threading.Thread(target=run, daemon=True).start()
