import time
import threading

from runtime_v7.core.distributed_cognition_v8 import CognitiveNodeV8
from runtime_v7.core.swarm_router_v772 import SwarmIntelligenceRouterV772
from runtime_v7.core.secure_cognitive_sync_v81 import SecureCognitiveSyncV81


class SwarmOSV81:
    def __init__(self):
        self.node = CognitiveNodeV8()
        self.router = SwarmIntelligenceRouterV772()
        self.crypto = SecureCognitiveSyncV81(self.node.node_id)

        self.running = True

    # -------------------------
    # CONNECT COGNITION → ROUTER
    # -------------------------
    def sync_to_router(self):
        while self.running:
            payload = self.node.get_payload()

            # update routing intelligence
            self.router.update_peer(
                node_id=self.node.node_id,
                latency=0.1,
                trust=payload["trust"],
                hops=1
            )

            time.sleep(2)

    # -------------------------
    # RECEIVE COGNITIVE PACKETS
    # -------------------------
    def receive_packet(self, packet):
        data = self.crypto.decrypt(packet)
        if not data:
            return

        self.node.merge_cognition(data)

    # -------------------------
    # BROADCAST COGNITION
    # -------------------------
    def broadcast_state(self):
        while self.running:
            payload = self.node.get_payload()
            secure = self.crypto.encrypt(payload)

            route = self.router.route("cognitive_sync")

            print("[SWARM OS] route:", route)
            print("[SWARM OS] packet:", secure)

            time.sleep(3)

    # -------------------------
    # START SWARM OS
    # -------------------------
    def start(self):
        threading.Thread(target=self.sync_to_router, daemon=True).start()
        threading.Thread(target=self.broadcast_state, daemon=True).start()

        self.node.start()

        print("[V8.1] Autonomous Swarm OS ONLINE")
