import subprocess
import time
import psutil

PROCESS_LIST = [
    "omega_v41_core.py",
    "omega_v42_autoreg.py",
    "omega_v43_state.py"
]

RESTART_COOLDOWN = {}

# ---------------------------
# CHECK PROCESS
# ---------------------------

def is_running(name):
    for p in psutil.process_iter():
        try:
            if name in p.cmdline():
                return True
        except:
            pass
    return False

# ---------------------------
# SAFE RESTART
# ---------------------------

def restart(name):
    now = time.time()

    if name in RESTART_COOLDOWN:
        if now - RESTART_COOLDOWN[name] < 10:
            return

    RESTART_COOLDOWN[name] = now

    print(f"[SUPERVISOR] Restarting {name}")

    subprocess.Popen(["python", name])

# ---------------------------
# MONITOR LOOP
# ---------------------------

def monitor():
    while True:
        for p in PROCESS_LIST:
            if not is_running(p):
                restart(p)

        time.sleep(5)

if __name__ == "__main__":
    monitor()
