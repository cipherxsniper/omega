import time
import traceback

print("[Ω-STABLE] Starting resilient Omega kernel...")

while True:
    try:
        print("[Ω-STABLE] Tick...")
        time.sleep(2)

    except Exception as e:
        print("[Ω-STABLE ERROR]", e)
        traceback.print_exc()
        time.sleep(1)
