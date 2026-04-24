from core.router import ModelRouter
from core.memory import Memory
from core.client import OllamaClient

print("🧠 DKF STABLE CORE v1 ONLINE")

memory = Memory()
client = OllamaClient()
router = ModelRouter(client)

while True:
    q = input("DKF > ").strip()
    if q in ["exit", "quit"]:
        break

    try:
        reply = router.generate(q, memory)
        print("\n🧠 RESPONSE:\n")
        print(reply)
        print("\n" + "-"*50 + "\n")
    except Exception as e:
        print("❌ FATAL ERROR:", e)
