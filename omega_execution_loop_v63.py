import time

class OmegaExecutionLoopV63:
    def __init__(self, kernel, registry, diagnostic, supervisor, temporal_gate, repair_action):
        self.kernel = kernel
        self.registry = registry
        self.diagnostic = diagnostic
        self.supervisor = supervisor
        self.temporal_gate = temporal_gate
        self.repair_action = repair_action

        self.running = False
        self.tick_id = 0

    # =========================
    # SINGLE SOURCE OF TRUTH LOOP
    # =========================
    def tick(self, event_type, module, score, drift):

        self.tick_id += 1

        # -------------------------
        # 1. REGISTRY UPDATE
        # -------------------------
        self.registry.tick(score, drift)

        # -------------------------
        # 2. DIAGNOSTIC UPDATE
        # -------------------------
        self.diagnostic.update(score, drift)
        needs = self.diagnostic.detect_needs()

        # -------------------------
        # 3. TEMPORAL GATE CHECK
        # -------------------------
        temporal = self.temporal_gate(self.registry, score, drift)

        # -------------------------
        # 4. SUPERVISOR DECISION
        # -------------------------
        decision = self.supervisor(event_type, module)

        # -------------------------
        # 5. REPAIR SIGNALING
        # -------------------------
        repair_result = None
        if "stability_recovery_required" in needs or "drift_dampening_required" in needs:
            repair_result = self.repair_action(event_type, module)

        # -------------------------
        # 6. STRUCTURED FEED OUTPUT
        # -------------------------
        return {
            "feed": self._feed(score, drift, needs),
            "needs": needs,
            "decision": decision,
            "repair": repair_result
        }

    # =========================
    # HUMAN-READABLE SYSTEM FEED
    # =========================
    def _feed(self, score, drift, needs):
        return f"""
[Ω EXECUTION LOOP v6.3]

TICK: {self.tick_id}

OBSERVATION:
- Score: {score}
- Drift: {drift}

REGISTRY STATE:
- Cycles: {self.registry.cycles}
- Memory: {self.registry.memory_records}

SYSTEM HEALTH:
- Coherence: {self.registry.coherence():.2f}

DIAGNOSTIC NEEDS:
- {', '.join(needs)}

INTERPRETATION:
- System is actively self-monitoring and routing corrections
"""
