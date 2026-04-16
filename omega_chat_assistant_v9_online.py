from omega_neural_bus_v9 import BUS
import time

def on_chat_message(msg):
    response = {
        "input": msg,
        "reply": "acknowledged via Nexus swarm mesh",
        "analysis": "event-driven cognition active",
    }
    print("[Ω CHAT]", response)

BUS.subscribe("chat.message", on_chat_message)

print("[Ω CHAT] ONLINE (event-driven, no input loop)")

while True:
    time.sleep(1)
