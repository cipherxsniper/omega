import math

MAX_SPEED = 2.5
DAMPING = 0.98

def stabilize(p):
    p["vx"] *= DAMPING
    p["vy"] *= DAMPING

    speed = math.sqrt(p["vx"]**2 + p["vy"]**2)

    if speed > MAX_SPEED:
        scale = MAX_SPEED / speed
        p["vx"] *= scale
        p["vy"] *= scale
