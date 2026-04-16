from omega_kernel_v6_8 import OmegaKernelV6_8
import time

k = OmegaKernelV6_8()

while True:
    out = k.tick()
    print(out)
    time.sleep(0.5)
