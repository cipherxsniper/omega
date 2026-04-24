from core.engine.dkf_engine import DKFEngine
from llm.client.ollama_client import OllamaClient

class Orchestrator:
    def __init__(self):
        self.llm = OllamaClient("llama3.2")
        self.engine = DKFEngine(self.llm)

    def chat(self):
        print("🧠 DKF PRODUCTION CORE ONLINE")

        while True:
            user = input("DKF > ")

            if user in ["exit", "quit"]:
                break

            response = self.engine.process(user)
            print("\n🧠", response, "\n")
