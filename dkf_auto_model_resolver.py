import requests

OLLAMA_URL = "http://127.0.0.1:11434"

class DKFModelResolver:
    def fetch_models(self):
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            return r.json().get("models", [])
        except:
            return []

    def score(self, m):
        name = m.get("name", "")

        if "tiny" in name:
            return 0
        if "1B" in name:
            return 1
        if "2B" in name:
            return 2
        if "7B" in name:
            return 5
        if "13B" in name:
            return 10
        return 99

    def select(self):
        models = self.fetch_models()
        if not models:
            return "tinyllama:latest"

        best = sorted(models, key=self.score)[0]
        return best.get("name", "tinyllama:latest")


def get_model():
    return DKFModelResolver().select()


if __name__ == "__main__":
    print(get_model())
