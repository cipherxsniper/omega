from runtime_v7.core.v9_9_swarm_bus import SwarmBusV99
from runtime_v7.core.v9_8_shared_memory_swarm_core import get_memory
import socket
import json

class LANSwarmV93:
    def __init__(self, port=6011):
        self.memory = get_memory()
        self.bus = SwarmBusV99()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))

    def start(self):
        print("[V9.3] BUS-ENABLED DISCOVERY ONLINE")

        while True:
            data, addr = self.sock.recvfrom(4096)
            msg = json.loads(data.decode())

            peer_id = msg.get("node_id", "unknown")

            self.memory.register_peer(peer_id, addr[0])

            # 🔥 EMIT EVENT INTO SWARM BUS
            self.bus.emit({
                "type": "peer_discovered",
                "node_id": peer_id,
                "ip": addr[0]
            })

if __name__ == "__main__":
    LANSwarmV93().start()
