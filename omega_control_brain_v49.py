from omega_self_diagnostic_v48 import OmegaSelfDiagnostic
from omega_temporal_drift_memory_v47 import temporal_causal_gate
from omega_supervisor_v42 import supervisor

# ================================
# Ω CONTROL BRAIN v4.9 (CORE LOOP)
# ================================

class OmegaControlBrain:
    def __init__(self):
        self.diagnostic = OmegaSelfDiagnostic()

    # ================================
    # MAIN ENTRY POINT
    # ================================
    def cycle(self, event_type, line, score=1.0, drift=0.0):

        # STEP 1 — UPDATE DIAGNOSTICS
        self.diagnostic.update(score, drift)
        needs = self.diagnostic.detect_needs()

        # STEP 2 — SUPERVISOR GATE FIRST
        decision = supervisor(event_type, line)

        # STEP 3 — CAUSAL DRIFT CHECK (v4.7)
        causal = temporal_causal_gate(self.diagnostic, score, drift)

        # STEP 4 — INTELLIGENCE FEED (READABLE STATE)
        feed = self.diagnostic.report()

        # STEP 5 — AUTO-REPAIR TRIGGERS (NO HARD BLOCKING)
        actions = []

        if "drift_dampening_required" in needs:
            actions.append("apply_drift_smoothing")

        if "stability_recovery_required" in needs:
            actions.append("apply_score_recovery")

        if "dependency_repair_required" in needs:
            actions.append("trigger_dependency_scan")

        if "threshold_relaxation_required" in needs:
            actions.append("adjust_dynamic_threshold")

        # ================================
        # FINAL OUTPUT (NO SILENT BLOCKING)
        # ================================
        return {
            "supervisor_decision": decision,
            "causal_state": causal,
            "diagnostic_feed": feed,
            "system_needs": needs,
            "recommended_actions": actions
        }
