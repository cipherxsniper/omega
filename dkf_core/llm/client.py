import requests

class OllamaClient:
    def __init__(self, model="llama3.2"):
        self.url = "http://127.0.0.1:11434/api/generate"
        self.model = model

    def generate(self, prompt):
        try:
            r = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            # HARD DEBUG (do NOT remove yet)
            print("\n[DEBUG RAW RESPONSE]:", r.text, "\n")

            data = r.json()

            if "error" in data:
                return f"[OLLAMA ERROR] {data['error']}"

            if "response" not in data:
                return f"[NO RESPONSE FIELD] {data}"

            text = data["response"]

            if not text or text.strip() == "":
                return "[EMPTY RESPONSE FROM MODEL] try different model or prompt"

            return text

        except Exception as e:
            return f"[REQUEST FAILED] {e}"
