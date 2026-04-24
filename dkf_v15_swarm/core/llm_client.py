import requests

class LLMClient:
    def __init__(self, model="tinyllama"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/generate"

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
            return r.json().get("response", "")
        except Exception as e:
            return f"[LLM ERROR] {e}"
