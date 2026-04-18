def clamp(x, min_v=-2.0, max_v=2.0):
    return max(min_v, min(max_v, x))

def stabilize(vx, vy):
    # damp extreme cognition feedback
    vx *= 0.98
    vy *= 0.98

    # hard clamp (prevents runaway explosion)
    vx = clamp(vx)
    vy = clamp(vy)

    return vx, vy
