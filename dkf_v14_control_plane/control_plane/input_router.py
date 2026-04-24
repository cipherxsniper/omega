class InputRouter:
    def __init__(self, process_manager, state):
        self.pm = process_manager
        self.state = state

    def handle(self, msg: str):
        msg = msg.strip()

        if msg in ["exit", "quit"]:
            self.pm.shutdown_all()
            exit()

        if msg == "status":
            print("🧠 Ollama:", self.state.ollama_active)
            return

        if msg == "reset":
            self.pm.shutdown_all()
            self.pm.bootstrap()
            return

        # default DKF reasoning stub
        print(f"🧠 DKF processing: {msg}")
