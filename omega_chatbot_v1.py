
import os
import time
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:1.5b"

# =========================
# COLORS (ChatGPT-like clean UI)
# =========================
GREEN = "\033[92m"
TEAL = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RESET = "\033[0m"

# =========================
# MEMORY (chat history)
# =========================
history = [
    {"role": "system", "content": "You are Omega AI OS V4. Be helpful, structured, and conversational like ChatGPT."}
]

# =========================
# SCREEN HELPERS
# =========================
def clear():
    os.system("clear")

def print_header():
    print(GREEN + "Omega AI OS V4" + RESET)
    print(GRAY + "ChatGPT-style terminal interface\n" + RESET)

# =========================
# STREAM SIMULATION (ChatGPT feel)
# =========================
def stream_print(text):
    for chunk in text.split():
        print(WHITE + chunk + " " + RESET, end="", flush=True)
        time.sleep(0.03)
    print("\n")

# =========================
# OLLAMA CALL (with memory)
# =========================
def ask_ollama(user_input):
    history.append({"role": "user", "content": user_input})

    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "messages": history,
        "stream": False
    })

    if r.status_code != 200:
        return f"Error: {r.text}"

    reply = r.json()["message"]["content"]

    history.append({"role": "assistant", "content": reply})
    return reply

# =========================
# UI LOOP (ChatGPT style)
# =========================
def main():
    clear()
    print_header()

    while True:
        user = input(TEAL + "You: " + RESET)

        if user.lower() in ["exit", "quit"]:
            break

        print(GRAY + "\nOmega is thinking...\n" + RESET)

        response = ask_ollama(user)

        print(GREEN + "Omega: " + RESET, end="")
        stream_print(response)

if __name__ == "__main__":
    main()
