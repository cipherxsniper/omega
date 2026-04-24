import requests
import sys
import json
from threading import Thread, Event
from queue import Queue

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


# =========================
# 🧠 SWARM MESSAGE BUS
# =========================
class SwarmBus:
    def __init__(self):
        self.subscribers = []
        self.queue = Queue()

    def publish(self, token):
        for sub in self.subscribers:
            sub.receive(token)

    def subscribe(self, agent):
        self.subscribers.append(agent)


# =========================
# 🧠 SWARM AGENT BASE
# =========================
class SwarmAgent:
    def __init__(self, name):
        self.name = name

    def receive(self, token):
        # lightweight reaction hook
        pass


# Example agents
class MemoryAgent(SwarmAgent):
    def receive(self, token):
        if "remember" in token.lower():
            print(f"\n🧠 [MEMORY] captured signal: {token}")


class CriticAgent(SwarmAgent):
    def receive(self, token):
        if "error" in token.lower():
            print(f"\n⚠️ [CRITIC] anomaly detected")


class EchoAgent(SwarmAgent):
    def receive(self, token):
        pass  # passive observer


# =========================
# 🧠 STREAM ENGINE
# =========================
def stream_generate(prompt, bus, model="tinyllama:latest"):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True
            },
            stream=True,
            timeout=120
        )

        print("\n🧠 RESPONSE:\n")

        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                chunk = json.loads(line)
                token = chunk.get("response", "")

                if token:
                    sys.stdout.write(token)
                    sys.stdout.flush()

                    # 🚀 SWARM BROADCAST
                    bus.publish(token)

                if chunk.get("done", False):
                    break

            except json.JSONDecodeError:
                continue

        print("\n")

    except Exception as e:
        print(f"\n[stream error] {e}")


# =========================
# 🧠 MAIN LOOP
# =========================
def main():
    print("🧠 DKF v2 STREAM SWARM BUS ONLINE")

    bus = SwarmBus()

    # register swarm agents
    bus.subscribe(MemoryAgent("memory"))
    bus.subscribe(CriticAgent("critic"))
    bus.subscribe(EchoAgent("echo"))

    while True:
        q = input("SWARM > ").strip()

        if not q:
            continue

        if q.lower() in ["exit", "quit"]:
            break

        stream_generate(q, bus)

        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
