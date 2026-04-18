import time
from omega_quantum_field_v23 import step, events, hubs
from omega_render_v11 import render

while True:
    step()
    render(events, hubs)
    time.sleep(0.1)
