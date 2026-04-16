import socket
import json
import threading


class CognitiveBusV7:

    def __init__(self, host="0.0.0.0", port=5050):
        self.host = host
        self.port = port
        self.peers = []

    def start_server(self, handler):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)

        print(f"[V7 BUS] Listening on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handler, args=(conn, addr)).start()

    def send(self, host, port, frame):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(json.dumps(frame).encode())
            s.close()
        except:
            pass
