import socket
import json
import time
import threading
from collections import defaultdict, deque


class SwarmPredictionV19:
    """
    V19 Swarm Prediction Engine

    Builds on V18 cognition:
    - predicts node behavior
    - forecasts failures
    - estimates swarm stability
    """

    def __init__(self, port=12019):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = f"pred-{int(time.time())}"

        # -------------------------
        # TIME SERIES MEMORY
        # -------------------------
        self.event_history = defaultdict(lambda: deque(maxlen=100))
        self.last_seen = {}

        # prediction state
        self.failure_risk = defaultdict(float)
        self.activity_trend = defaultdict(list)

        self.running = True

        print(f"[V19 PREDICTION] ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # EVENT PROCESSING
    # -------------------------
    def process_event(self, event):
        node = event.get("node_id")
        etype = event.get("type")
        now = time.time()

        self.event_history[node].append((etype, now))
        self.last_seen[node] = now

        self._update_trends(node)
        self._update_failure_risk(node, etype)

    # -------------------------
    # TREND TRACKING
    # -------------------------
    def _update_trends(self, node):
        history = self.event_history[node]

        heartbeats = sum(1 for e, _ in history if e == "heartbeat")

        self.activity_trend[node].append(heartbeats)

        # keep small rolling window
        if len(self.activity_trend[node]) > 20:
            self.activity_trend[node] = self.activity_trend[node][-20:]

    # -------------------------
    # FAILURE RISK MODEL
    # -------------------------
    def _update_failure_risk(self, node, etype):
        if etype == "heartbeat":
            self.failure_risk[node] *= 0.95  # decay risk
        elif etype in ("spam", "invalid"):
            self.failure_risk[node] += 0.2
        else:
            self.failure_risk[node] += 0.05

        # time decay (node silence = risk increases)
        if node in self.last_seen:
            silence = time.time() - self.last_seen[node]

            if silence > 10:
                self.failure_risk[node] += 0.1

            if silence > 30:
                self.failure_risk[node] += 0.3

    # -------------------------
    # PREDICT NEXT STATE
    # -------------------------
    def predict_node_state(self, node):
        risk = self.failure_risk[node]

        trend = self.activity_trend[node]
        growth = 0

        if len(trend) >= 2:
            growth = trend[-1] - trend[0]

        if risk > 1.5:
            return "high_failure_probability"

        if risk > 0.8:
            return "unstable_node"

        if growth > 5:
            return "high_activity_node"

        if growth < 0:
            return "declining_node"

        return "stable_node"

    # -------------------------
    # SWARM FORECAST
    # -------------------------
    def swarm_forecast(self):
        total = len(self.failure_risk)

        high_risk = sum(1 for v in self.failure_risk.values() if v > 1.0)
        unstable = sum(1 for v in self.failure_risk.values() if 0.5 < v <= 1.0)

        stability = 1.0

        if total > 0:
            stability = 1.0 - (high_risk / total)

        return {
            "nodes": total,
            "high_risk": high_risk,
            "unstable": unstable,
            "stability_score": round(stability, 3)
        }

    # -------------------------
    # LISTENER
    # -------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                print(f"[V19 EVENT] {event}")

                self.process_event(event)

            except Exception as e:
                print(f"[V19 ERROR] {e}")

    # -------------------------
    # INSIGHT LOOP
    # -------------------------
    def insight_loop(self):
        while self.running:
            forecast = self.swarm_forecast()

            print(f"[V19 FORECAST] {forecast}")

            # per-node predictions
            for node in list(self.failure_risk.keys())[:5]:
                state = self.predict_node_state(node)
                print(f"[V19 PREDICT] {node} → {state}")

            time.sleep(5)

    # -------------------------
    # START
    # -------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.insight_loop, daemon=True)

        t1.start()
        t2.start()

        print("[V19 PREDICTION] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    SwarmPredictionV19().start()
