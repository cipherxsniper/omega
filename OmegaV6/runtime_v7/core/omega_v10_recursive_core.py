import time
import hashlib
import hmac
import json
import threading
from collections import defaultdict

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt
from runtime_v7.core.omega_semantic_model_v1 import SemanticModelV1


class OmegaV10RecursiveCore:

    def __init__(self):
        print("\n🧠 [V10 CORE] INITIALIZING RECURSIVE COGNITION ENGINE...\n")

        # -------------------------
        # MEMORY + SEMANTICS
        # -------------------------
        self.memory = get_crdt()
        self.semantic = SemanticModelV1()

        # -------------------------
        # NODE IDENTITY
        # -------------------------
        self.node_id = self._id()
        self.secret = b"omega-v10-core-key"

        # -------------------------
        # COGNITIVE STATE
        # -------------------------
        self.last_index = 0
        self.running = True

        self.trust = defaultdict(lambda: 1.0)

        # patch system (safe evolution)
        self.patch_queue = []
        self.applied_patches = []

        # reasoning hooks (modular cognition)
        self.brain = {
            "interpreters": [self.default_interpret],
            "evaluators": [self.evaluate_thought]
        }

        # safety limits
        self.max_memory_scan = 300
        self.max_patch_queue = 50

        # start loops
        threading.Thread(target=self.cognition_loop, daemon=True).start()
        threading.Thread(target=self.patch_loop, daemon=True).start()

        print(f"\n🧠 [V10 CORE] ONLINE | NODE={self.node_id}\n")

    # -------------------------
    # IDENTITY
    # -------------------------
    def _id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.secret, raw, hashlib.sha256).hexdigest()

    def verify(self, event):
        if "signature" not in event:
            return False
        expected = self.sign({k: v for k, v in event.items() if k != "signature"})
        return hmac.compare_digest(expected, event["signature"])

    # -------------------------
    # SEMANTIC ENGINE
    # -------------------------
    def default_interpret(self, event):
        return self.semantic.interpret(event)

    # -------------------------
    # THOUGHT EVALUATION
    # -------------------------
    def evaluate_thought(self, thought):
        confidence = thought.get("confidence", 0.5)

        if confidence > 0.85:
            return {
                "type": "reinforce",
                "strength": 0.02,
                "reason": "high signal coherence"
            }

        if confidence < 0.25:
            return {
                "type": "decay",
                "strength": -0.02,
                "reason": "low signal instability"
            }

        return None

    # -------------------------
    # PATCH SYSTEM (SAFE EVOLUTION)
    # -------------------------
    def patch_loop(self):
        while self.running:
            try:
                if self.patch_queue:

                    patch = self.patch_queue.pop(0)

                    print(f"[V10 CORE PATCH] {patch}")

                    if patch["type"] == "reinforce":
                        self.trust["system"] *= 1.001

                    elif patch["type"] == "decay":
                        self.trust["system"] *= 0.999

                    self.applied_patches.append(patch)

                time.sleep(2)

            except Exception as e:
                print("[V10 PATCH ERROR]", e)

    # -------------------------
    # MAIN COGNITION LOOP
    # -------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.state.get("events", [])
                events = events[-self.max_memory_scan:]

                new_events = events[self.last_index:]
                self.last_index = len(events)

                for event in new_events:

                    # interpret
                    thought = self.default_interpret(event)

                    print(f"[V10 THOUGHT] {thought}")

                    # evaluate
                    patch = self.evaluate_thought(thought)

                    if patch and len(self.patch_queue) < self.max_patch_queue:
                        self.patch_queue.append(patch)

                time.sleep(1)

            except Exception as e:
                print("[V10 COGNITION ERROR]", e)

    # -------------------------
    # EXTERNAL INPUT ENTRYPOINT
    # -------------------------
    def ingest(self, event):
        event["node_id"] = self.node_id
        event["timestamp"] = time.time()
        event["signature"] = self.sign(event)
        self.memory.apply(event)

    # -------------------------
    # STATUS
    # -------------------------
    def status(self):
        return {
            "node_id": self.node_id,
            "trust": dict(self.trust),
            "patches_applied": len(self.applied_patches),
            "queue_size": len(self.patch_queue)
        }
