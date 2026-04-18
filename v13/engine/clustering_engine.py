from nodes.identity_node import IdentityNode

event_hubs = []

def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def hub_similarity(a, b):
    return abs(a.state["coherence"] - b.state["coherence"]) + \
           abs(a.state["entropy"] - b.state["entropy"])


def find_or_create_hub(event):
    global event_hubs

    for hub in event_hubs:
        if distance(hub, event) < 4:

            if isinstance(event, dict):
                hub.integrate(event)

            return hub

    new_hub = IdentityNode(event["x"], event["y"])
    new_hub.integrate(event)
    event_hubs.append(new_hub)

    return new_hub


def merge_hubs():
    global event_hubs

    merged = set()
    new_list = []

    for i in range(len(event_hubs)):
        if i in merged:
            continue

        a = event_hubs[i]

        for j in range(i + 1, len(event_hubs)):
            if j in merged:
                continue

            b = event_hubs[j]

            if hub_similarity(a, b) < 0.3:
                # merge b into a
                a.strength += b.strength
                a.members += b.members
                a.history.extend(b.history)

                merged.add(j)

        new_list.append(a)

    event_hubs[:] = new_list


def update_hubs():
    for h in event_hubs:
        h.decay()

    merge_hubs()

    # cleanup dead hubs
    event_hubs[:] = [h for h in event_hubs if not h.is_dead()]
