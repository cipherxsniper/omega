import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "tinyllama:latest"


class ChatEngine:
    def __init__(self):
        self.memory = []

    def prompt(self, user):
        history = "\n".join(self.memory[-8:])

        return f"""
You are DKF CORE v1 — a stable reasoning intelligence.

You must:
- respond clearly
- think step-by-step internally
- ask a follow-up question every time

Memory:
{history}

User: {user}
DKF:
"""

    def ask(self, user):
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": self.prompt(user),
                    "stream": False
                },
                timeout=60
            )
            return r.json()["response"]

        except Exception as e:
            return f"[ERROR] {e}"

    def run(self):
        print("🧠 DKF CORE CHAT ONLINE")

        while True:
            q = input("DKF > ").strip()

            if q in ["exit", "quit"]:
                break

            res = self.ask(q)
            print("\n🧠", res, "\n")

            self.memory.append(f"User: {q}")
            self.memory.append(f"DKF: {res}")


if __name__ == "__main__":
    ChatEngine().run()
