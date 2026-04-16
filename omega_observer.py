import json
import time
import os

print("👁️ OMEGA OBSERVER ONLINE\n")

def read_file(path):
    try:
        with open(path) as f:
            return f.readlines()[-10:]
    except:
        return []

while True:
    core = read_file("logs/core.log")
    node = read_file("logs/node.log")
    py = read_file("logs/python.log")

    print("\n================ OMEGA STATUS ================")

    print("🧠 CORE INTELLIGENCE:")
    for line in core:
        print(" - Swarm Activity:", line.strip())

    print("\n⚙️ NODE ACTIVITY:")
    for line in node:
        print(" - JS Worker:", line.strip())

    print("\n🐍 PYTHON INTELLIGENCE:")
    for line in py:
        print(" - AI Brain:", line.strip())

    print("==============================================\n")

    time.sleep(2)
