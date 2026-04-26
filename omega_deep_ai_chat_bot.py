import requests
import subprocess
import sys
import time
import random
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"

# ---------------- COLORS ----------------
RESET = "\033[0m"
GREEN = "\033[92m"
TEAL = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"

PROMPT = TEAL + "~Ωmega€¥§:" + RESET + " "

# ---------------- HEADER ----------------
def banner():
    print(TEAL + "\n~Ωmega€¥§ OS v2 STREAM ONLINE" + RESET)
    print(GREEN + "Mode: Live AI Streaming + Binary Visual Engine\n" + RESET)

# ---------------- COLOR BINARY RAIN ----------------
def thinking():
    chars = ["0", "1", "Ω", "█", "▓", "▒", "░"]
    colors = [GREEN, BLUE, MAGENTA, YELLOW, TEAL]

    for _ in range(10):
        line = ""
        for _ in range(60):
            c = random.choice(chars)
            color = random.choice(colors)
            line += color + c + RESET
        sys.stdout.write("\rΩ thinking: " + line)
        sys.stdout.flush()
        time.sleep(0.04)

    print("\r" + " " * 120 + "\r", end="")

# ---------------- REAL STREAMING AI ----------------
def stream_ai(prompt):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": True
            },
            stream=True,
            timeout=120
        )

        print("\nΩ RESPONSE:\n")

        full = ""

        for line in r.iter_lines():
            if not line:
                continue

            try:
                import json
                data = json.loads(line.decode("utf-8"))

                token = ""
                if "response" in data:
                    token = data["response"]

                # TYPE EFFECT (REAL STREAM)
                for c in token:
                    sys.stdout.write(GREEN + c + RESET)
                    sys.stdout.flush()
                    time.sleep(0.008)

                full += token

            except:
                continue

        print("\n")
        return full

    except Exception as e:
        return f"[STREAM ERROR] {e}"

# ---------------- COMMANDS ----------------
def ls():
    return subprocess.getoutput("ls -la")

def scan():
    root = "/data/data/com.termux/files/home/omega"
    count = 0
    for _, _, files in os.walk(root):
        count += len(files)
    return f"📂 Omega Files: {count}"

def run(file):
    path = os.path.join("/data/data/com.termux/files/home/omega", file)
    if not os.path.exists(path):
        return "❌ file not found"
    return subprocess.getoutput(f"python {path}")

# ---------------- ROUTER ----------------
def handle(cmd):
    cmd = cmd.strip()

    if cmd == "exit":
        return "EXIT"

    if cmd == "ls":
        return ls()

    if cmd == "scan":
        return scan()

    if cmd.startswith("run "):
        return run(cmd[4:])

    return None

# ---------------- MAIN ----------------
banner()

while True:
    user = input(PROMPT)

    result = handle(user)

    if result == "EXIT":
        break

    if result is not None:
        print(result)
        continue

    # 🌐 THINKING VISUAL
    thinking()

    # 🧠 STREAMING AI
    stream_ai(user)

    print("-" * 60)
    print("TIME:", datetime.now().isoformat())
