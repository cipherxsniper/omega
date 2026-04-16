import time

class OmegaRuntimeRegistryV62:
    def __init__(self):
        self.start_time = time.time()

        self.nodes = set()
        self.brains = set()
        self.modules = set()

        self.memory_records = 0
        self.cycles = 0

        self.last_drift = 0
        self.last_score = 0

    # =========================
    # SYSTEM REGISTRATION
    # =========================
    def register_node(self, node_id):
        self.nodes.add(node_id)

    def register_brain(self, brain_id):
        self.brains.add(brain_id)

    def register_module(self, module_name):
        self.modules.add(module_name)

    def tick(self, score, drift):
        self.cycles += 1
        self.memory_records += 1

        self.last_score = score
        self.last_drift = drift

    # =========================
    # SYSTEM HEALTH METRICS
    # =========================
    def coherence(self):
        if self.cycles == 0:
            return 1.0
        return max(0.0, min(1.0, self.last_score - (self.last_drift * 0.01)))

    def uptime(self):
        return time.time() - self.start_time

    # =========================
    # LIVE FEED OUTPUT
    # =========================
    def feed(self):
        return f"""
[Ω RUNTIME REGISTRY v6.2]

Uptime: {self.uptime():.2f}s

NODES:
- {len(self.nodes)}

BRAINS:
- {len(self.brains)}

MODULES:
- {len(self.modules)}

EXECUTION:
- Cycles: {self.cycles}
- Memory Records: {self.memory_records}

LATEST STATE:
- Score: {self.last_score}
- Drift: {self.last_drift}

SYSTEM HEALTH:
- Coherence: {self.coherence():.2f}
"""
