import socket
import threading
import time

class NodeDiscovery:
    def __init__(self, port=6001):
        self.port = port
        self.nodes = set()
        self.running = True

    def scan_ip(self, ip):
        try:
            s = socket.socket()
            s.settimeout(0.2)
            s.connect((ip, self.port))
            self.nodes.add(ip)
            s.close()
        except:
            pass

    def discover(self):
        base_ip = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:-1])

        while self.running:
            threads = []

            for i in range(1, 255):
                ip = f"{base_ip}.{i}"
                t = threading.Thread(target=self.scan_ip, args=(ip,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            time.sleep(10)

    def start(self):
        t = threading.Thread(target=self.discover, daemon=True)
        t.start()
