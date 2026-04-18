# ==================================================
# 🧠 OMEGA QUANTUM FIELD v13+ (MOTION UPGRADE)
# Identity Node + Force Field Architecture
# ==================================================

import random
import uuid

# -----------------------------
# CONFIG
# -----------------------------
WIDTH = 60
HEIGHT = 25

EVENT_DECAY = 10
HUB_DECAY = 25

# -----------------------------
# STATE
# -----------------------------
events = []
hubs = []

# ==================================================
# UTILS
# ==================================================

def uid():
    return str(uuid.uuid4())[:8]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

# ==================================================
# EVENT SYSTEM
# ==================================================

def emit_event():
    return {
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 1),
        "strength": random.random(),
        "life": EVENT_DECAY,
        "merged": False
    }

# ==================================================
# IDENTITY NODE SYSTEM (◆)
# ==================================================

def create_hub(x, y, strength):
    return {
        "id": uid(),
        "x": float(x),
        "y": float(y),

        # MOTION STATE (NEW)
        "vx": 0.0,
        "vy": 0.0,

        # IDENTITY VECTOR
        "state": {
            "activation": strength,
            "stability": 0.1,
            "coherence": 0.1,
            "momentum": 0.0,
            "entropy": 0.2,
        },

        "strength": strength,
        "members": 1,
        "life": HUB_DECAY,
        "history": []
    }


def integrate_event(hub, event):
    s = event["strength"]

    hub["strength"] += s
    hub["members"] += 1

    st = hub["state"]

    st["activation"] = clamp(st["activation"] + s * 0.2)
    st["coherence"] = clamp(st["coherence"] + 0.03)
    st["stability"] = clamp(st["stability"] + 0.01)
    st["entropy"] = clamp(st["entropy"] * 0.98)

    dx = event["x"] - hub["x"]
    dy = event["y"] - hub["y"]
    st["momentum"] += (dx + dy) * 0.001

    hub["history"].append(s)


def hub_similarity(a, b):
    return (
        abs(a["state"]["coherence"] - b["state"]["coherence"]) +
        abs(a["state"]["entropy"] - b["state"]["entropy"])
    )


def update_hub_state(h):
    st = h["state"]

    st["activation"] *= 0.95
    st["entropy"] += 0.01
    st["entropy"] -= st["stability"] * 0.02

    st["entropy"] = clamp(st["entropy"])
    st["activation"] = clamp(st["activation"])

    h["life"] -= 1


# ==================================================
# FIELD FORCES (NEW CORE PHYSICS)
# ==================================================

def apply_field_forces(event):
    for h in hubs:
        dx = h["x"] - event["x"]
        dy = h["y"] - event["y"]

        dist = max(1, abs(dx) + abs(dy))
        force = h["state"]["activation"] / dist

        event["x"] += dx * 0.02 * force
        event["y"] += dy * 0.02 * force


def hub_interactions():
    for a in hubs:
        for b in hubs:
            if a == b:
                continue

            dx = b["x"] - a["x"]
            dy = b["y"] - a["y"]

            dist = max(1, abs(dx) + abs(dy))
            pull = b["state"]["activation"] / dist

            a["vx"] += dx * 0.001 * pull
            a["vy"] += dy * 0.001 * pull


def update_hub_motion(h):
    st = h["state"]

    # entropy drift
    h["vx"] += (random.random() - 0.5) * st["entropy"] * 0.3
    h["vy"] += (random.random() - 0.5) * st["entropy"] * 0.3

    # stability damping
    h["vx"] += (0 - h["vx"]) * st["stability"] * 0.05
    h["vy"] += (0 - h["vy"]) * st["stability"] * 0.05

    # momentum carry
    h["vx"] += st["momentum"] * 0.01
    h["vy"] += st["momentum"] * 0.01

    # apply motion
    h["x"] += h["vx"]
    h["y"] += h["vy"]

    # bounds
    h["x"] = max(0, min(WIDTH - 1, h["x"]))
    h["y"] = max(0, min(HEIGHT - 1, h["y"]))


# ==================================================
# CLUSTER ENGINE
# ==================================================

def update_clusters():
    global events, hubs

    for e in events:
        if e["merged"]:
            continue

        best = None
        best_d = 999

        for h in hubs:
            d = distance(h, e)
            if d < best_d:
                best_d = d
                best = h

        if best and best_d < 4:
            integrate_event(best, e)
            e["merged"] = True
        else:
            hubs.append(create_hub(e["x"], e["y"], e["strength"]))
            e["merged"] = True


# ==================================================
# CLEANUP
# ==================================================

def decay():
    global hubs, events

    for e in events:
        e["life"] -= 1

    events = [e for e in events if e["life"] > 0]

    for h in hubs:
        update_hub_state(h)
        h["life"] -= 1

    hubs = [h for h in hubs if h["life"] > 0]


# ==================================================
# RENDER
# ==================================================

def render():
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for e in events:
        x = int(e["x"])
        y = int(e["y"])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = "✦"

    for h in hubs:
        x = int(h["x"])
        y = int(h["y"])

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            st = h["state"]

            if st["entropy"] > 0.7:
                symbol = "◇"
            elif st["activation"] > 0.6:
                symbol = "◆"
            else:
                symbol = "◇"

            grid[y][x] = symbol

    for row in grid:
        print("".join(row))


# ==================================================
# STEP ENGINE
# ==================================================

def step():
    global events

    for _ in range(random.randint(5, 12)):
        events.append(emit_event())

    for e in events:
        apply_field_forces(e)

    update_clusters()
    hub_interactions()

    for h in hubs:
        update_hub_state(h)
        update_hub_motion(h)

    decay()
    render()


# ==================================================
# MAIN LOOP
# ==================================================

if __name__ == "__main__":
    print("\n🧠 OMEGA v13+ — IDENTITY FIELD WITH MOTION\n")

    for tick in range(20):
        print(f"\n--- TICK {tick} ---")
        step()

    print("\n🧠 SYSTEM COMPLETE")
