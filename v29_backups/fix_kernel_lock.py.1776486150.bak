import os

LOCK_FILE = os.path.expanduser("~/Omega/.omega_kernel.lock")
os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)


def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            print(f"[KERNEL V1] Already running (PID {pid}) → exiting")
        except:
            print("[KERNEL V1] Already running → exiting")
        return False

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

    return True


def release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass
