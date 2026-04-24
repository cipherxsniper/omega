from controller import OllamaController

class DKF:
    def __init__(self):
        self.ollama = OllamaController()
        self.memory = []

    def chat(self, prompt, model="tinyllama"):
        print(f"🧠 DKF > {prompt}")

        response = self.ollama.run(model, prompt)

        self.memory.append({
            "input": prompt,
            "output": response
        })

        return response
