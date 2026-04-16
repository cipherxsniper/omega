import socket
import json
import threading

class OmegaBusV3:
    def __init__(self, port=5060):
        self.port = port
        self.handlers = []

    def on_message(self, fn):
        self.handlers.append(fn)

    def start(self):
        def server():
            s = socket.socket()
            s.bind(("0.0.0.0", self.port))
            s.listen(10)

            print(f"[Ω-BUS v3] listening on {self.port}")

            while True:
                conn, _ = s.accept()
                data = conn.recv(8192).decode()

                try:
                    msg = json.loads(data)
                    for h in self.handlers:
                        h(msg)
                except:
                    pass

                conn.close()

        import threading
        threading.Thread(target=server, daemon=True).start()

    def send(self, host, port, msg):
        try:
            s = socket.socket()
            s.connect((host, port))
            s.send(json.dumps(msg).encode())
            s.close()
        except:
            pass
