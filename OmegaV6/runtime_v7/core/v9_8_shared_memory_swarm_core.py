import time
import threading

class SharedSwarmMemory:
    def __init__(self):
        self.peers = {}
        self.trusted = set()
        self.lock = threading.Lock()

    def register_peer(self, peer_id, ip):
        with self.lock:
            self.peers[peer_id] = {"ip": ip, "last_seen": time.time()}
        print(f"[MEMORY] peer registered {peer_id} @ {ip}")

    def mark_trusted(self, node_id):
        with self.lock:
            self.trusted.add(node_id)
        print(f"[MEMORY] trusted node {node_id}")

    def get_trusted_nodes(self):
        with self.lock:
            return list(self.trusted)

def get_memory():
    return SharedSwarmMemory()
