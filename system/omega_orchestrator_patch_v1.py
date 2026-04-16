from system.omega_schema_guard_v1 import normalize_rec

def safe_step(recursive_engine):
    rec = recursive_engine.step()

    rec = normalize_rec(rec)

    return rec
