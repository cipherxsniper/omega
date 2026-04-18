import random

# 🧠 v16 QUANTUM TRACE LAYER
traces = []

def emit_trace(x, y):
    if random.random() < 0.35:
        traces.append({
            "x": x,
            "y": y,
            "life": random.randint(3, 8)
        })

def decay_traces():
    for t in traces:
        t["life"] -= 1
    traces[:] = [t for t in traces if t["life"] > 0]
