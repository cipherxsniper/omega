import socket
import json
import time
import threading
from collections import defaultdict


class SwarmCoordinationV21:
    """
    V21 Swarm Coordination Layer

    Turns optimization swarm into a coordinated system:
    - shared intents
    - consensus voting
    - global decision alignment
    """

    def __init__(self, port=14021):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = f"coord-{int(time.time())}"

        # -------------------------
        # GLOBAL SWARM STATE
        # -------------------------
        self.nodes = set()
        self.trust = defaultdict(lambda: 1.0)
        self.performance = defaultdict(lambda: 1.0)

        # shared intent system
        self.intents = {}  # intent_id -> payload
        self.votes = defaultdict(lambda: defaultdict(float))  # intent_id -> node -> score

        self.running = True

        print(f"[V21 COORD] ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # EVENT HANDLER
    # -------------------------
    def process_event(self, event):
        node = event.get("node_id")
        etype = event.get("type")

        if not node:
            return

        self.nodes.add(node)

        # update simple trust model
        if etype == "heartbeat":
            self.trust[node] += 0.01
        elif etype in ("spam", "invalid"):
            self.trust[node] -= 0.2

        self.trust[node] = max(0.0, min(2.0, self.trust[node]))

    # -------------------------
    # INTENT CREATION
    # -------------------------
    def create_intent(self, action, priority=1.0):
        intent_id = f"intent-{int(time.time() * 1000)}"

        self.intents[intent_id] = {
            "action": action,
            "priority": priority,
            "timestamp": time.time()
        }

        print(f"[V21 INTENT] created {intent_id} → {action}")

        return intent_id

    # -------------------------
    # VOTING SYSTEM
    # -------------------------
    def vote(self, node, intent_id, score):
        weight = self.trust[node] * self.performance[node]
        self.votes[intent_id][node] = score * weight

    # -------------------------
    # CONSENSUS ENGINE
    # -------------------------
    def compute_consensus(self, intent_id):
        votes = self.votes[intent_id]

        if not votes:
            return 0

        total_weight = sum(votes.values())
        node_count = len(votes)

        consensus = total_weight / node_count

        return round(consensus, 3)

    # -------------------------
    # DECISION ENGINE
    # -------------------------
    def decide_actions(self):
        decisions = []

        for intent_id in list(self.intents.keys()):
            consensus = self.compute_consensus(intent_id)

            intent = self.intents[intent_id]

            if consensus > 1.0:
                decisions.append((intent_id, "EXECUTE", intent["action"]))
            elif consensus < 0.3:
                decisions.append((intent_id, "REJECT", intent["action"]))
            else:
                decisions.append((intent_id, "DEFER", intent["action"]))

        return decisions

    # -------------------------
    # LISTENER
    # -------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                print(f"[V21 EVENT] {event}")

                self.process_event(event)

            except Exception as e:
                print(f"[V21 ERROR] {e}")

    # -------------------------
    # COORDINATION LOOP
    # -------------------------
    def coordination_loop(self):
        while self.running:

            decisions = self.decide_actions()

            print("\n[V21 DECISIONS]")
            for intent_id, action, payload in decisions:
                print(f" - {intent_id}: {action} → {payload}")

            time.sleep(5)

    # -------------------------
    # START
    # -------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.coordination_loop, daemon=True)

        t1.start()
        t2.start()

        print("[V21 COORD] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    SwarmCoordinationV21().start()
