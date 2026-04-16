from omega_core_state_v61 import OmegaCoreState
from collections import deque
import time

class OmegaUnifiedKernelV6:
from omega_runtime_registry_v62 import OmegaRuntimeRegistryV62
    def __init__(self, supervisor, repair_action, temporal_gate, diagnostic):
        self.registry = OmegaRuntimeRegistryV62()
        self.memory = OmegaCoreState()
        self.supervisor = supervisor
        self.repair_action = repair_action
        self.temporal_gate = temporal_gate
        self.diagnostic = diagnostic

        self.scores = deque(maxlen=50)
        self.drifts = deque(maxlen=50)

        self.threshold = 0.75

    # ================================
    # CORE INGEST LOOP
    # ================================
    def ingest(self, event_type, module, score, drift, line=""):
        self.registry.tick(score, drift)
        self.scores.append(score)
        self.drifts.append(drift)

        avg_score = sum(self.scores) / len(self.scores)
        avg_drift = sum(self.drifts) / len(self.drifts)

        velocity = self._velocity()

        # ================================
        # ADAPTIVE THRESHOLD ENGINE (v5.1 core)
        # ================================
        if velocity < -0.05:
            self.threshold *= 0.98
        elif velocity > 0:
            self.threshold *= 1.01

        # ================================
        # SELF STABILIZATION
        # ================================
        self._stabilize()

        # ================================
        # SUPERVISOR GATE
        # ================================
        decision = self.supervisor(event_type, line)

        # ================================
        # CAT REPAIR LAYER
        # ================================
        if decision == "approve" and event_type == "missing_module":
            self.repair_action(event_type, {"module": module})

        # ================================
        # TEMPORAL GATE
        # ================================
        temporal = self.temporal_gate(self, score, drift)

        # ================================
        # DIAGNOSTIC FEED
        # ================================
        needs = self.diagnostic.detect_needs()

        return {
        feed = self.registry.feed()
            "feed": self._feed(event_type, module, score, drift, avg_score, avg_drift, velocity),
            "needs": needs,
            "threshold": self.threshold,
            "decision": decision,
            "temporal": temporal
        }

    # ================================
    # SELF STABILIZATION LOOP
    # ================================
    def _stabilize(self):
        if len(self.drifts) == 0:
            return

        avg_drift = sum(self.drifts) / len(self.drifts)

        # drift damping
        if avg_drift > 25:
            self.drifts = deque([d * 0.95 for d in self.drifts], maxlen=50)

        # score smoothing (soft recovery pulse)
        if len(self.scores) > 0 and avg_drift > 30:
            self.scores = deque([min(1.0, s + 0.01) for s in self.scores], maxlen=50)

    # ================================
    # VELOCITY MODEL
    # ================================
    def _velocity(self):
        if len(self.scores) < 2:
            return 0.0
        feed = self.registry.feed()
        return self.scores[-1] - self.scores[0]
        feed = self.registry.feed()

    # ================================
    # READABLE INTELLIGENCE FEED
    # ================================
    def _feed(self, event_type, module, score, drift, avg_score, avg_drift, velocity):
        return f"""
        feed = self.registry.feed()
[Ω UNIFIED COGNITIVE KERNEL v6]

Event:
- Type: {event_type}
- Target: {module}

Observation:
- Score: {score:.2f}
- Drift: {drift}

System State:
- Avg Score: {avg_score:.2f}
- Avg Drift: {avg_drift:.2f}
- Velocity: {velocity:.4f}
- Threshold: {self.threshold:.2f}

Interpretation:
- System is actively self-regulating

Status:
- CAT repair active
- Supervisor gate active
- Temporal model active
- Stabilization loop active
"""
