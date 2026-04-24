import requests
from core.config import OLLAMA_URL, TIMEOUT

class OllamaClient:
    def generate(self, model, prompt, timeout=TIMEOUT):
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )

        try:
            data = r.json()
        except Exception:
            return f"[JSON ERROR] {r.text}"

        return data.get("response", "[EMPTY RESPONSE]")
