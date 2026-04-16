import socket
import json
import time
import threading
import uuid
from collections import defaultdict

# =========================
# 🧬 V13 SWARM REASONING ENGINE
# =========================

class SwarmReasoningV13:
    def __init__(self, port=6060):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        # 🧠 GRAPH STRUCTURES
        self.events = {}              # event_id -> event data
        self.edges = defaultdict(lambda: defaultdict(int))  # A -> B -> weight
        self.sequence_buffer = []

        print(f"[V13] SWARM REASONING ONLINE | port={self.port}")

    # -------------------------
    # 🧠 STORE EVENT
    # -------------------------
    def store_event(self, event):
        eid = str(uuid.uuid4())[:8]
        self.events[eid] = event

        self.sequence_buffer.append(eid)

        # keep buffer small
        if len(self.sequence_buffer) > 10:
            self.sequence_buffer.pop(0)

        # build causal edges
        self.build_causal_links()

    # -------------------------
    # 🔗 CAUSAL INFERENCE
    # -------------------------
    def build_causal_links(self):
        if len(self.sequence_buffer) < 2:
            return

        for i in range(len(self.sequence_buffer) - 1):
            a = self.sequence_buffer[i]
            b = self.sequence_buffer[i + 1]

            self.edges[a][b] += 1

    # -------------------------
    # 🧠 FIND STRONGEST CAUSE PATH
    # -------------------------
    def infer_path(self):
        if not self.edges:
            return None

        strongest = None
        max_weight = 0

        for a, targets in self.edges.items():
            for b, w in targets.items():
                if w > max_weight:
                    max_weight = w
                    strongest = (a, b)

        return strongest, max_weight

    # -------------------------
    # 🌐 PROCESS MESSAGE
    # -------------------------
    def process(self, msg):
        self.store_event(msg)

        path = self.infer_path()

        if path:
            (a, b), w = path
            print(f"[V13 CAUSAL] {a} → {b} | weight={w}")

        print(f"[V13 EVENT] {msg}")

    # -------------------------
    # 🌐 LISTENER
    # -------------------------
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(4096)

            try:
                msg = json.loads(data.decode())
            except:
                continue

            self.process(msg)

    # -------------------------
    # 🚀 START
    # -------------------------
    def start(self):
        print("[V13] STARTING SWARM REASONING ENGINE")

        t = threading.Thread(target=self.listen, daemon=True)
        t.start()

        while True:
            time.sleep(10)
            print(
                f"[V13 STATUS] events={len(self.events)} "
                f"edges={sum(len(v) for v in self.edges.values())}"
            )


if __name__ == "__main__":
    SwarmReasoningV13().start()
