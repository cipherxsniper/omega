import socket
import json
import threading

class OmegaBus:
    """
    Lightweight ZeroMQ replacement for Termux compatibility
    """

    def __init__(self, port=5055):
        self.port = port
        self.peers = []
        self.running = True

    def start_server(self, handler):
        def server():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("0.0.0.0", self.port))
            s.listen(5)

            print(f"[Ω-BUS] listening on {self.port}")

            while self.running:
                conn, addr = s.accept()
                data = conn.recv(4096).decode()

                try:
                    msg = json.loads(data)
                    handler(msg)
                except:
                    pass

                conn.close()

        t = threading.Thread(target=server, daemon=True)
        t.start()

    def send(self, host, port, msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(json.dumps(msg).encode())
            s.close()
        except:
            pass
