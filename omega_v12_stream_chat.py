import requests
import sys
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def stream_generate(prompt, model="tinyllama:latest"):
    try:
        response = requests.post(
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

        full_text = ""

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            try:
                chunk = json.loads(line)

                token = chunk.get("response", "")

                if token:
                    sys.stdout.write(token)
                    sys.stdout.flush()
                    full_text += token

                if chunk.get("done", False):
                    break

            except json.JSONDecodeError:
                # skip malformed stream packets safely
                continue

        print("\n")
        return full_text

    except Exception as e:
        return f"[stream error] {e}"


print("🧠 Omega Streaming Kernel Online (v12)")

while True:
    try:
        q = input("Ω > ").strip()

        if not q:
            continue

        if q.lower() in ["exit", "quit"]:
            print("🧠 shutting down...")
            break

        stream_generate(q)

        print("\n" + "-" * 50 + "\n")

    except KeyboardInterrupt:
        print("\n🧠 forced shutdown")
        break
