def classify(value):
    if value < 0:
        return "unstable"
    elif value < 0.3:
        return "low"
    elif value < 0.7:
        return "medium"
    else:
        return "high"
