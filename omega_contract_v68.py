def omega_contract(*, health, output, signals):
    if not isinstance(health, (int, float)):
        raise ValueError("health must be float")

    if health < 0: health = 0.0
    if health > 1: health = 1.0

    return {
        "health": float(health),
        "output": output,
        "signals": signals if isinstance(signals, dict) else {}
    }
