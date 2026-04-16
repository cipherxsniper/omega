import socket


class LANDiscoveryV86:
    def scan_local_network(self, port=6001):
        found = []

        base = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:-1])

        for i in range(1, 255):
            ip = f"{base}.{i}"

            try:
                s = socket.socket()
                s.settimeout(0.2)
                s.connect((ip, port))
                found.append(ip)
                s.close()
            except:
                pass

        return found
