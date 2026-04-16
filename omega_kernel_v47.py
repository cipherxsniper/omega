import time
import signal

RUNNING = True

def shutdown(signum, frame):
    global RUNNING
    print("[KERNEL] Shutdown signal received")
    RUNNING = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def main():
    print("[KERNEL] ONLINE")

    while RUNNING:
        try:
            print("[KERNEL] heartbeat")
            time.sleep(3)
        except:
            time.sleep(1)

    print("[KERNEL] HALTED")

if __name__ == "__main__":
    main()
