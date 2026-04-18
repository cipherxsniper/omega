import subprocess

SERVICES = [
    "omega_v46_router.py",
    "omega_v47_scheduler.py",
    "omega_v48_plugins.py",
    "omega_v49_crdt.py"
]

# ---------------------------
# BOOT SYSTEM
# ---------------------------

def boot():
    print("🧠 OMEGA OS KERNEL STARTING\n")

    for s in SERVICES:
        print(f"Launching {s}")
        subprocess.Popen(["python", s])

    print("\n✔ Omega OS ONLINE")

# ---------------------------
# START
# ---------------------------

if __name__ == "__main__":
    boot()
