
def pressure(node):
    mem = len(node.get("context", []))
    influence = node.get("influence", 0.5)

    # core evolutionary forces
    exploration = 1 - influence
    saturation = min(1.0, mem / 50)

    return (exploration * 0.6) + (saturation * 0.4)


def state(p):
    if p > 0.75:
        return "SPLIT"
    if p > 0.5:
        return "ADAPT"
    if p > 0.25:
        return "LEARN"
    return "STABLE"
