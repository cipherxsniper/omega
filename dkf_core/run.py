from llm.client import OllamaClient
from memory.memory import Memory
from core.engine import DKFEngine

def main():
    print("🧠 DKF CORE v1 ONLINE (Stable System)")
    print("⚡ Connected to Ollama + Memory Layer\n")

    llm = OllamaClient(model="llama3.2")
    memory = Memory()
    engine = DKFEngine(llm, memory)

    while True:
        user = input("DKF > ").strip()

        if user in ["exit", "quit"]:
            break

        response = engine.run(user)

        print("\n🧠", response, "\n")

if __name__ == "__main__":
    main()
