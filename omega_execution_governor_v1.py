import time
import signal
import sys

RUNNING = True

def shutdown(signum, frame):
    global RUNNING
    print("[EXECUTION GOV] Shutdown signal received")
    RUNNING = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def main():
    print("[EXECUTION GOV] ACTIVE")

    # 🔁 REQUIRED: persistent runtime loop
    while RUNNING:
        try:
            # Simulated execution control logic
            print("[EXECUTION GOV] regulating execution...")
            time.sleep(2)

        except Exception as e:
            print(f"[EXECUTION GOV] ERROR: {e}")
            time.sleep(2)

    print("[EXECUTION GOV] CLEAN EXIT")

if __name__ == "__main__":
    main()
