import requests
import time
import os

URL = "http://127.0.0.1:8080"

def wait_for_server():
    while True:
        try:
            requests.get(URL + "/status", timeout=1)
            return
        except:
            print("⏳ Waiting for Omega cluster API...")
            time.sleep(2)

def render():
    os.system("clear")

    try:
        status = requests.get(URL + "/status").json()
        nodes = requests.get(URL + "/nodes").json()

        print("🧠 OMEGA CLUSTER DASHBOARD v51\n")

        print("📊 SYSTEM STATE (READABLE ENGLISH)")
        print(f"- Cluster status: {status['status']}")
        print(f"- Total Python nodes detected: {status['total_nodes']}")
        print(f"- System time: {status['time']}\n")

        print("📦 ACTIVE NODES SAMPLE:")
        for n in nodes.get("nodes", [])[:10]:
            print(f"- Node file acting as worker: {n}")

        print("\n🧠 INTERPRETATION:")
        print("System is functioning as a file-based distributed execution graph.")

    except Exception as e:
        print("Dashboard error:", e)

if __name__ == "__main__":
    wait_for_server()

    while True:
        render()
        time.sleep(3)
