# FIX: normalize trace format for Omega v7.5

def normalize_trace(trace):
    if isinstance(trace, dict) and "trace" in trace:
        return trace["trace"]
    return trace
