from omega_v7_core import OmegaV7
import time

omega = OmegaV7()

tick = 0

while True:
    tick += 1
    result = omega.step(tick)
    print(result)
    time.sleep(0.2)
