import time
import json
import uuid
import hashlib
import threading


class CognitiveNodeV8:
    def __init__(self, node_id=None):
        self.node_id = node_id or self._generate_id()

        # 🧠 shared cognitive state
        self.memory = []
        self.shared_beliefs = {}
        self.task_queue = []

        # 🌐 mesh state
        self.peers = {}
        self.trust_scores = {}

        # ⚡ cognition tuning
        self.cognition_tick = 2
        self.running = True

    # -------------------------
    # IDENTITY
    # -------------------------
    def _generate_id(self):
        raw = f"{uuid.uuid4()}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # -------------------------
    # MEMORY SYSTEM
    # -------------------------
    def remember(self, event):
        self.memory.append({
            "event": event,
            "timestamp": time.time()
        })

        # keep memory bounded
        if len(self.memory) > 500:
            self.memory = self.memory[-500:]

    # -------------------------
    # DISTRIBUTED COGNITION MERGE
    # -------------------------
    def merge_cognition(self, remote_payload):
        node = remote_payload.get("node_id")
        if not node:
            return

        # update peer presence
        self.peers[node] = time.time()

        # merge shared beliefs
        beliefs = remote_payload.get("beliefs", {})
        for k, v in beliefs.items():
            self.shared_beliefs[k] = (
                self.shared_beliefs.get(k, 0) * 0.7 + v * 0.3
            )

        self.remember(f"merged cognition from {node}")

    # -------------------------
    # TASK DELEGATION ENGINE
    # -------------------------
    def add_task(self, task):
        self.task_queue.append({
            "task": task,
            "created": time.time(),
            "status": "queued"
        })

    def process_tasks(self):
        while self.running:
            if self.task_queue:
                task = self.task_queue.pop(0)
                task["status"] = "processing"

                self.remember(f"processing task: {task['task']}")

                # simulate distributed decision making
                score = len(task["task"]) % 10

                task["score"] = score
                task["status"] = "complete"

                self.remember(f"completed task: {task['task']} score={score}")

            time.sleep(self.cognition_tick)

    # -------------------------
    # TRUST SYSTEM
    # -------------------------
    def update_trust(self, node_id, delta):
        self.trust_scores[node_id] = self.trust_scores.get(node_id, 1.0) + delta

        # clamp
        self.trust_scores[node_id] = max(0.1, min(10.0, self.trust_scores[node_id]))

    # -------------------------
    # COGNITIVE BROADCAST PAYLOAD
    # -------------------------
    def get_payload(self):
        return {
            "node_id": self.node_id,
            "beliefs": self.shared_beliefs,
            "trust": self.trust_scores.get(self.node_id, 1.0),
            "memory_size": len(self.memory),
            "timestamp": time.time()
        }

    # -------------------------
    # COGNITION LOOP
    # -------------------------
    def cognition_loop(self):
        while self.running:
            self.remember("cognition_tick")

            # weak self-learning update
            self.shared_beliefs["system_health"] = (
                self.shared_beliefs.get("system_health", 0.5) * 0.99 + 0.01
            )

            time.sleep(self.cognition_tick)

    # -------------------------
    # START SYSTEM
    # -------------------------
    def start(self):
        threading.Thread(target=self.process_tasks, daemon=True).start()
        threading.Thread(target=self.cognition_loop, daemon=True).start()

        self.remember("V8 cognition mesh started")
        print("[V8] Distributed cognition mesh ONLINE")
