# ================================
# Ω TEMPORAL DRIFT MEMORY v4.7 FIXED CONTRACT
# ================================

def temporal_causal_gate(memory, score, drift):
    """
    Unified memory contract version.
    Requires OmegaCoreState-compatible object.
    """

    # HARD SAFETY CHECK (prevents silent crashes)
    if not hasattr(memory, "record"):
        raise TypeError("[Ω TEMPORAL] Invalid memory object: missing record()")

    memory.record(score, drift)

    avg_score = memory.avg_score()
    avg_drift = memory.avg_drift()

    velocity = 0.0
    if len(memory.scores) > 1:
        velocity = memory.scores[-1] - memory.scores[0]

    trend = "stable"
    if velocity < -0.05:
        trend = "degrading"
    elif velocity > 0.05:
        trend = "improving"

    return {
        "avg_score": avg_score,
        "avg_drift": avg_drift,
        "velocity": velocity,
        "trend": trend
    }
