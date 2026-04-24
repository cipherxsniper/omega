import requests

class OllamaClient:
    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://127.0.0.1:11434/api/generate"

    def generate(self, prompt):
        r = requests.post(self.url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return r.json().get("response", "[no response]")
