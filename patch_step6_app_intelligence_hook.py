# STEP 6 — OMEGA INTELLIGENCE CORE HOOK

from omega_intelligence_core import omega_process

def generate_reply(intent, message, history):
    """
    Replaces legacy reply system with Omega semantic intelligence core.
    """

    # Build structured reasoning output
    response = omega_process(message)

    return response
