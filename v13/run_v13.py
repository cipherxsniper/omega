from engine.main_loop import step
from engine.clustering_engine import event_hubs
from visual.render import render_grid

import random
import time

def simulate():
    for _ in range(200):
        # fake event stream
        from core.event_system import emit_event
        emit_event(
            random.randint(0, 50),
            random.randint(0, 20),
            random.random()
        )

        step()
        render_grid(event_hubs)

        time.sleep(0.05)

if __name__ == "__main__":
    simulate()
