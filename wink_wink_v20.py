import time
from omega_global_thought_bus_v23 import run_observer

while True:
    try:
        print(run_observer("$file"))
        time.sleep(1)
    except KeyboardInterrupt:
        break
