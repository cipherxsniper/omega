def normalize_rec(rec):
    if not isinstance(rec, dict):
        return {
            "agents": {},
            "strongest": "brain_0",
            "status": "error",
            "timestamp": 0
        }

    rec.setdefault("agents", {
        "brain_0": 0,
        "brain_1": 0,
        "brain_2": 0,
        "brain_3": 0
    })

    rec.setdefault("status", "active")
    rec.setdefault("timestamp", __import__("time").time())

    # compute strongest safely
    try:
        rec["strongest"] = max(rec["agents"], key=rec["agents"].get)
    except Exception:
        rec["strongest"] = "brain_0"

    return rec
