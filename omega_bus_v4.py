import socket
import json
import threading

class OmegaBusV4:
    def __init__(self, port=5070):
        self.port = port
        self.handlers = []

    def on_message(self, fn):
        self.handlers.append(fn)

    def start(self):
        def run():
            s = socket.socket()
            s.bind(("0.0.0.0", self.port))
            s.listen(20)

            print(f"[Ω-BUS v4] ACTIVE on {self.port}")

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

    def send(self, host, port, msg):
        try:
            s = socket.socket()
            s.connect((host, port))
            s.send(json.dumps(msg).encode())
            s.close()
        except:
            pass
