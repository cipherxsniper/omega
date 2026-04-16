# Ω CHAT v9.4 — EVENT ONLY (NO input(), NO blocking)

import time
from omega_event_bus_v9_4 import consume

def chat_loop():
    print("[Ω CHAT] event mode online")

    while True:
        msg = consume("chat.message")

        if not msg:
            time.sleep(0.1)
            continue

        print("[CHAT RX]", msg)
        print("[CHAT TX]", f"processed: {msg}")


if __name__ == "__main__":
    chat_loop()
