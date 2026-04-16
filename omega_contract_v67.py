def omega_contract(health: float, output=None, signals=None):
    """
    Ω v6.7 Autonomic Control Contract

    Every Omega module MUST return through this function.
    """

    if signals is None:
        signals = {}

    # HARD ENFORCEMENT: normalize types
    try:
        health = float(health)
    except:
        health = 0.0

    return {
        "health": max(0.0, min(1.0, health)),
        "output": output,
        "signals": signals
    }
