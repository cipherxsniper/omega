from core.event_system import drain_events
from engine.clustering_engine import find_or_create_hub, update_hubs

def step():
    events = drain_events()

    for e in events:
        find_or_create_hub(e)

    update_hubs()
