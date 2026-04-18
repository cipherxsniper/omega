def normalize_influence(influence):
    if isinstance(influence, dict):
        return float(influence.get("flow_x", 0.0)), float(influence.get("flow_y", 0.0))

    if isinstance(influence, (list, tuple)):
        fx = influence[0] if len(influence) > 0 else 0.0
        fy = influence[1] if len(influence) > 1 else 0.0
        return float(fx), float(fy)

    try:
        v = float(influence)
    except:
        v = 0.0

    return v, v
