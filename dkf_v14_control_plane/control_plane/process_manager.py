import subprocess
import os

class ProcessManager:
    def __init__(self, state):
        self.state = state

    def bootstrap(self):
        print("⚙️ Bootstrapping DKF services...")
        self.start_ollama()

    def start_ollama(self):
        if self.state.ollama_active:
            return

        print("🤖 Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"])
        self.state.ollama_active = True

    def stop_all_python(self):
        print("🧹 Killing Python processes (Termux-safe)...")
        os.system("pkill -f python")

    def stop_ollama(self):
        print("🧹 Stopping Ollama...")
        os.system("pkill -f ollama")

    def shutdown_all(self):
        print("🛑 DKF shutdown initiated...")
        self.stop_all_python()
        self.stop_ollama()
