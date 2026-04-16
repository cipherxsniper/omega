import socket
import json
import time
import threading
from collections import defaultdict, deque


class SwarmOptimizationV20:
    """
    V20 Swarm Self-Optimization Engine

    Evolves from prediction → action:
    - adjusts trust dynamically
    - optimizes node routing weights
    - self-heals based on predicted risk
    """

    def __init__(self, port=13020):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = f"opt-{int(time.time())}"

        # -------------------------
        # STATE
        # -------------------------
        self.trust = defaultdict(lambda: 1.0)
        self.performance = defaultdict(lambda: 1.0)
        self.failure_risk = defaultdict(float)

        self.event_history = defaultdict(lambda: deque(maxlen=50))

        self.running = True

        print(f"[V20 OPTIMIZER] ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # PROCESS EVENT
    # -------------------------
    def process_event(self, event):
        node = event.get("node_id")
        etype = event.get("type")

        self.event_history[node].append(etype)

        # update risk baseline (simplified from V19 logic)
        if etype == "heartbeat":
            self.failure_risk[node] *= 0.9
            self.performance[node] += 0.01

        elif etype in ("spam", "invalid"):
            self.failure_risk[node] += 0.3
            self.performance[node] -= 0.1

        else:
            self.performance[node] += 0.001

        # clamp values
        self.trust[node] = max(0.0, min(2.0, self.trust[node]))
        self.performance[node] = max(0.1, min(3.0, self.performance[node]))

    # -------------------------
    # OPTIMIZATION ENGINE
    # -------------------------
    def optimize(self):
        for node in list(self.trust.keys()):

            risk = self.failure_risk[node]
            perf = self.performance[node]

            # 🔻 penalize risky nodes
            if risk > 1.0:
                self.trust[node] -= 0.2

            # 🔺 reward stable nodes
            if risk < 0.3:
                self.trust[node] += 0.1

            # performance feedback loop
            if perf > 1.5:
                self.trust[node] += 0.05

            if perf < 0.5:
                self.trust[node] -= 0.1

            # auto-repair drift
            if self.trust[node] < 0.2:
                print(f"[V20 OPT] isolating unstable node={node}")

            if self.trust[node] > 1.8:
                print(f"[V20 OPT] promoting high-performance node={node}")

    # -------------------------
    # ROUTING WEIGHT ENGINE
    # -------------------------
    def routing_weights(self):
        weights = {}

        for node in self.trust:
            score = (
                self.trust[node] * 0.5 +
                self.performance[node] * 0.3 +
                (1.0 - self.failure_risk[node]) * 0.2
            )

            weights[node] = round(score, 3)

        return weights

    # -------------------------
    # LISTENER
    # -------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)
                event = json.loads(data.decode())

                print(f"[V20 EVENT] {event}")

                self.process_event(event)

            except Exception as e:
                print(f"[V20 ERROR] {e}")

    # -------------------------
    # OPTIMIZER LOOP
    # -------------------------
    def optimizer_loop(self):
        while self.running:
            self.optimize()

            weights = self.routing_weights()

            print(f"[V20 WEIGHTS] {weights}")

            time.sleep(5)

    # -------------------------
    # START
    # -------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.optimizer_loop, daemon=True)

        t1.start()
        t2.start()

        print("[V20 OPTIMIZER] STARTED")

        while True:
            time.sleep(1)


if __name__ == "__main__":
    SwarmOptimizationV20().start()
