import socket
import json
import time
import threading
from collections import defaultdict, deque


class SwarmCognitionV18:
    """
    V18 Swarm Cognition Layer

    Adds:
    - memory graph of swarm events
    - causal linking
    - behavioral reasoning
    - anomaly detection
    """

    def __init__(self, port=11018):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = f"cog-{int(time.time())}"

        # -------------------------
        # MEMORY GRAPH
        # -------------------------
        self.event_graph = defaultdict(list)     # node → events
        self.causal_links = defaultdict(list)    # event_id → related events
        self.history = deque(maxlen=5000)

        # trust / behavior model
        self.behavior_score = defaultdict(lambda: 0)

        self.running = True

        print(f"[V18 COGNITION] ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # EVENT ID
    # -------------------------
    def _event_id(self, event):
        return f"{event.get('node_id')}:{event.get('type')}:{event.get('timestamp')}"

    # -------------------------
    # LISTEN LOOP
    # -------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                eid = self._event_id(event)

                print(f"[V18 EVENT] {event}")

                self.history.append(event)
                self.event_graph[event.get("node_id")].append(event)

                self._update_behavior(event)
                self._build_causal_links(event)

            except Exception as e:
                print(f"[V18 ERROR] {e}")

    # -------------------------
    # BEHAVIOR MODELING
    # -------------------------
    def _update_behavior(self, event):
        node = event.get("node_id")
        etype = event.get("type")

        if etype == "heartbeat":
            self.behavior_score[node] += 1

        elif etype in ("spam", "invalid"):
            self.behavior_score[node] -= 3

        else:
            self.behavior_score[node] += 0.2

    # -------------------------
    # CAUSAL LINKING ENGINE
    # -------------------------
    def _build_causal_links(self, event):
        if len(self.history) < 2:
            return

        current = self._event_id(event)
        previous = self._event_id(self.history[-2])

        # simple temporal causality assumption
        self.causal_links[current].append(previous)

    # -------------------------
    # ANOMALY DETECTION
    # -------------------------
    def detect_anomalies(self):
        anomalies = []

        for node, score in self.behavior_score.items():
            if score < -5:
                anomalies.append((node, "malicious_pattern"))
            elif score > 50:
                anomalies.append((node, "high_activity"))

        return anomalies

    # -------------------------
    # REASONING ENGINE
    # -------------------------
    def reason_about_node(self, node):
        events = self.event_graph[node]

        heartbeats = sum(1 for e in events if e["type"] == "heartbeat")
        other = len(events) - heartbeats

        score = self.behavior_score[node]

        if score < -3:
            return "high-risk-node"

        if heartbeats > other:
            return "stable-beacon-node"

        if len(events) > 20:
            return "active-participant"

        return "unknown-pattern"

    # -------------------------
    # INSIGHT LOOP
    # -------------------------
    def insight_loop(self):
        while self.running:
            anomalies = self.detect_anomalies()

            print(f"[V18 INSIGHT] nodes={len(self.event_graph)} anomalies={len(anomalies)}")

            for node, reason in anomalies:
                print(f"[V18 ANOMALY] {node} → {reason}")

            time.sleep(5)

    # -------------------------
    # START
    # -------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.insight_loop, daemon=True)

        t1.start()
        t2.start()

        print("[V18 COGNITION] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    SwarmCognitionV18().start()
