import socket

class PortManagerV82:
    def __init__(self, base_port=6000):
        self.base_port = base_port
        self.used = set()

    def get_free_port(self):
        for port in range(self.base_port, self.base_port + 100):
            if port in self.used:
                continue

            try:
                s = socket.socket()
                s.bind(("0.0.0.0", port))
                s.close()
                self.used.add(port)
                return port
            except:
                continue

        raise RuntimeError("No free ports available")
