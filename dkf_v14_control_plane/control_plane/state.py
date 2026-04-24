class DKFState:
    def __init__(self):
        self.processes = {}
        self.running = True
        self.ollama_active = False
        self.swarm_active = False
