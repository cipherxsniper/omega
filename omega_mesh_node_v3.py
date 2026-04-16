import time
import random
import json
import socket


class OmegaMeshNodeV3:

    def __init__(self, node_id):
        self.node_id = node_id
        self.peers = []
        self.state = self.boot()

    # ------------------------
    # BOOT
    # ------------------------
    def boot(self):
        return {
            "node_id": self.node_id,
            "agents": {
                "brain_0": random.uniform(40, 60),
                "brain_1": random.uniform(40, 60),
                "brain_2": random.uniform(40, 60),
                "brain_3": random.uniform(40, 60)
            },
            "strongest": None,
            "timestamp": time.time(),
            "memory_delta": [],
            "node_health": 100.0
        }

    # ------------------------
    # LOCAL THINKING
    # ------------------------
    def step(self):
        s = self.state

        for b in s["agents"]:
            s["agents"][b] += random.uniform(-2, 2)

        s["strongest"] = max(s["agents"], key=s["agents"].get)

        s["memory_delta"].append({
            "t": time.time(),
            "strongest": s["strongest"]
        })

        s["node_health"] = min(100.0, s["node_health"] + random.uniform(-1, 1))
        s["timestamp"] = time.time()

        return s

    # ------------------------
    # MESH SYNC (PSEUDO PROTOCOL)
    # ------------------------
    def broadcast(self, peer_nodes):
        packet = self.step()

        for peer in peer_nodes:
            try:
                peer.receive(packet)
            except:
                continue

    def receive(self, packet):
        # merge cognition (soft consensus)
        for k in self.state["agents"]:
            self.state["agents"][k] = (
                self.state["agents"][k] * 0.7 +
                packet["agents"][k] * 0.3
            )

        self.state["memory_delta"].append({
            "sync_from": packet["node_id"],
            "strongest": packet["strongest"]
        })
