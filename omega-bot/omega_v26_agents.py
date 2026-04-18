class Agent:

    def __init__(self, name):
        self.name = name
        self.state = {}

    def analyze(self, input_text):

        tokens = input_text.lower().split()

        return {
            "agent": self.name,
            "tokens": tokens,
            "signal": len(tokens)
        }

    def propose_change(self, analysis):

        return {
            "agent": self.name,
            "proposal": f"optimize_{analysis['signal']}"
        }
