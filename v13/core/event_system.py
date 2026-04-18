
events = []

def emit_event(x, y, strength):
    events.append({
        "x": x,
        "y": y,
        "strength": strength
    })


def drain_events():
    global events
    temp = events
    events = []
    return temp
