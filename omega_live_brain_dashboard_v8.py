import json
import time
import os

BUS_FILE = "omega_bus_data.json"

def load():
    if not os.path.exists(BUS_FILE):
        return {}
    try:
        with open(BUS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def render(data):
    os.system("clear")

    print("🧠 OMEGA LIVE BRAIN DASHBOARD v8")
    print("="*40)

    for node, info in data.items():
        val = info["data"]
        bar = "█" * int(val * 10)

        print(f"{node}")
        print(f"  value: {round(val,3)}")
        print(f"  activity: {bar}")
        print("")

while True:
    d = load()
    render(d)
    time.sleep(1)
