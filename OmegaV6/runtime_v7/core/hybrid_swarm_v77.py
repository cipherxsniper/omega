import time

class HybridSwarmV77:
    def __init__(self):
        self.lan_peers = {}
        self.relay_peers = {}
        self.routing_table = {}

    def route_message(self, msg, target):
        if target in self.lan_peers:
            self.send_lan(msg, target)

        elif target in self.relay_peers:
            self.send_relay(msg, target)

        else:
            self.broadcast_mesh(msg)

    def update_routing(self, node_id, hops, strength):
        self.routing_table[node_id] = {
            "hops": hops,
            "signal": strength,
            "last_seen": time.time()
        }

    def broadcast_mesh(self, msg):
        for peer in self.lan_peers:
            self.send_lan(msg, peer)

        for relay in self.relay_peers:
            self.send_relay(msg, relay)
