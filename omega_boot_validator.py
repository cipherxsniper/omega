import os

REQUIRED = [
    "core/omega_neural_bus_v9_4.py",
    "core/__init__.py"
]

print("[Ω VALIDATOR] Checking system...")

failed = False

for path in REQUIRED:
    if not os.path.exists(path):
        print(f"[FAIL] Missing: {path}")
        failed = True
    else:
        print(f"[OK] {path}")

if failed:
    print("[Ω VALIDATOR] SYSTEM NOT SAFE TO START")
    exit(1)
else:
    print("[Ω VALIDATOR] ALL SYSTEMS GO")

