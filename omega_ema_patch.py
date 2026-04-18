# =========================
# COGNITION STABILIZER (EMA)
# =========================

alpha = 0.2
prev_avg = None

def smooth_avg(avg):
    global prev_avg

    if prev_avg is None:
        prev_avg = avg
        return avg

    avg = alpha * avg + (1 - alpha) * prev_avg
    prev_avg = avg
    return avg
