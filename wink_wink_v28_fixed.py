import time
from omega_global_thought_bus_v24 import run_observer

while True:
    try:
        print(run_observer("wink_wink_v28"))
        time.sleep(1)
    except KeyboardInterrupt:
        break
