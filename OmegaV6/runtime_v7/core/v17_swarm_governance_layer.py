import socket
import json
import time
import threading
import uuid


class SwarmGovernanceV17:
    """
    V17 Autonomous Swarm Governance Layer

    Adds:
    - trust scoring governance
    - automatic banning/promotions
    - quorum-based decisions
    - self-healing swarm rules
    """

    def __init__(self, port=10017):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = str(uuid.uuid4())[:12]

        # swarm state
        self.trust_score = {}
        self.banned_nodes = set()
        self.active_nodes = set()

        self.rules = {
            "ban_threshold": -3,
            "promote_threshold": 5
        }

        self.running = True

        print(f"[V17 GOV] ONLINE | node={self.node_id} | port={self.port}")

    # -----------------------------
    # RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                node = event.get("node_id")
                etype = event.get("type")

                if node in self.banned_nodes:
                    print(f"[V17 BLOCKED] banned node {node}")
                    continue

                print(f"[V17 EVENT] {event}")

                self.active_nodes.add(node)

                self.apply_governance(node, etype)

            except Exception as e:
                print(f"[V17 ERROR] {e}")

    # -----------------------------
    # GOVERNANCE ENGINE
    # -----------------------------
    def apply_governance(self, node, etype):
        if node not in self.trust_score:
            self.trust_score[node] = 0

        # scoring rules
        if etype == "heartbeat":
            self.trust_score[node] += 1

        elif etype == "invalid":
            self.trust_score[node] -= 2

        elif etype == "spam":
            self.trust_score[node] -= 3

        # enforce rules
        score = self.trust_score[node]

        if score <= self.rules["ban_threshold"]:
            self.ban_node(node)

        elif score >= self.rules["promote_threshold"]:
            self.promote_node(node)

    # -----------------------------
    # BAN NODE
    # -----------------------------
    def ban_node(self, node):
        self.banned_nodes.add(node)
        self.active_nodes.discard(node)

        print(f"[V17 GOVERNANCE] ❌ BANNED node={node}")

    # -----------------------------
    # PROMOTE NODE
    # -----------------------------
    def promote_node(self, node):
        print(f"[V17 GOVERNANCE] ⭐ PROMOTED node={node}")

    # -----------------------------
    # QUORUM CHECK
    # -----------------------------
    def quorum_met(self):
        return len(self.active_nodes) > 2

    # -----------------------------
    # SELF-HEAL LOOP
    # -----------------------------
    def self_heal(self):
        while self.running:
            if not self.quorum_met():
                print("[V17 HEAL] quorum low → relaxing rules temporarily")
                self.rules["ban_threshold"] = -5
            else:
                self.rules["ban_threshold"] = -3

            time.sleep(5)

    # -----------------------------
    # START
    # -----------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.self_heal, daemon=True)

        t1.start()
        t2.start()

        print("[V17 GOV] STARTED")

        while True:
            print(f"[V17 STATUS] active={len(self.active_nodes)} banned={len(self.banned_nodes)}")
            time.sleep(5)


if __name__ == "__main__":
    SwarmGovernanceV17().start()
