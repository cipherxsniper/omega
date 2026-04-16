import time

files = {
    "core": "Omega/Omega_v9/omega_v10/logs/core.log",
    "node": "Omega/Omega_v9/omega_v10/logs/node.log",
    "python": "Omega/Omega_v9/omega_v10/logs/python.log"
}

def tail(path):
    try:
        with open(path) as f:
            return f.readlines()[-5:]
    except:
        return []

while True:
    print("\n🧠 OMEGA OBSERVER (TRANSLATED INTELLIGENCE)")
    print("=====================================")

    for name, path in files.items():
        print(f"\n🔹 {name.upper()} SYSTEM:")
        for line in tail(path):
            clean = line.strip()

            # BASIC TRANSLATION LAYER
            if "Swarm" in clean:
                print("➡️ Swarm intelligence update detected:", clean)
            elif "ONLINE" in clean:
                print("➡️ System status:", clean)
            else:
                print("➡️ Activity:", clean)

    print("\n=====================================\n")

    time.sleep(2)
