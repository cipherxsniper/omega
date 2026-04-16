import time
from collections import defaultdict

class OmegaMemoryFederationV28:
    def __init__(self):
        self.event_memory = []
        self.consensus_memory = []
        self.experience_memory = defaultdict(list)
        self.meta_memory = []

        self.step = 0

    # ---------------------------
    # STORE EVENT
    # ---------------------------
    def store_event(self, event):
        self.event_memory.append({
            "ts": time.time(),
            "event": event
        })

        if len(self.event_memory) > 500:
            self.event_memory = self.event_memory[-500:]

    # ---------------------------
    # STORE CONSENSUS (FROM V27)
    # ---------------------------
    def store_consensus(self, consensus):
        self.consensus_memory.append({
            "ts": time.time(),
            "consensus": consensus
        })

        if len(self.consensus_memory) > 300:
            self.consensus_memory = self.consensus_memory[-300:]

    # ---------------------------
    # STORE EXPERIENCE FEEDBACK
    # ---------------------------
    def store_experience(self, brain, outcome):
        self.experience_memory[brain].append({
            "ts": time.time(),
            "outcome": outcome
        })

        if len(self.experience_memory[brain]) > 100:
            self.experience_memory[brain] = self.experience_memory[brain][-100:]

    # ---------------------------
    # GENERATE META INSIGHT
    # ---------------------------
    def generate_meta_insight(self):
        if len(self.consensus_memory) < 10:
            return None

        recent = self.consensus_memory[-10:]

        stability = 0.0
        last = None

        for r in recent:
            c = r["consensus"]
            if last is not None:
                stability += abs(c.get("value", 0) - last.get("value", 0))
            last = c

        insight = {
            "type": "stability_index",
            "value": stability / len(recent)
        }

        self.meta_memory.append(insight)

        return insight

    # ---------------------------
    # FEDERATED READ
    # ---------------------------
    def read_global_memory(self):
        return {
            "events": self.event_memory[-20:],
            "consensus": self.consensus_memory[-20:],
            "meta": self.meta_memory[-10:]
        }

    # ---------------------------
    # MAIN STEP
    # ---------------------------
    def step_cycle(self):
        self.step += 1

        meta = self.generate_meta_insight()

        return {
            "step": self.step,
            "meta_insight": meta,
            "memory_size": {
                "events": len(self.event_memory),
                "consensus": len(self.consensus_memory)
            }
        }
