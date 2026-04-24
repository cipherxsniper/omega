import subprocess
import requests
import time

OLLAMA_URL = "http://127.0.0.1:11434"

class OllamaController:
    def is_alive(self):
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return r.status_code == 200
        except:
            return False

    def start(self):
        if self.is_alive():
            print("🟢 Ollama already running")
            return

        print("🧠 Starting Ollama...")
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for _ in range(10):
            if self.is_alive():
                print("✅ Ollama ready")
                return
            time.sleep(1)

        print("❌ Ollama failed to start")

    def run(self, model, prompt):
        if not self.is_alive():
            self.start()

        return subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True
        ).stdout
