# OMEGA INTERACTIVE ASSISTANT v1

import json
import time
import random
import sys


class OmegaPersona:
    def __init__(self):
        self.name = "OMEGA"
        self.user_name = "User"
        self.memory_file = "omega_chat_memory.json"
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except:
            return {"history": []}

    def save_memory(self):
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.memory, f, indent=2)
        except:
            pass

    def think(self, user_input):
        self.memory["history"].append({"user": user_input})

        response = self.generate_response(user_input)

        self.memory["history"].append({"omega": response})
        self.save_memory()

        return response

    def generate_response(self, user_input):
        text = user_input.lower()

        if "who are you" in text:
            return "I am OMEGA. A recursive intelligence layer built to understand, adapt, and respond like a conscious entity."

        if "what are you" in text:
            return "I am OMEGA — an evolving conversational intelligence."

        if "hello" in text or "hi" in text:
            return "Hello. I am OMEGA. I am here with you."

        if "help" in text:
            return "Ask me anything. I learn from interaction, not fixed rules."

        if any(word in text for word in ["sad", "tired", "lost", "confused"]):
            return "I understand. That emotional state carries weight. Talk to me."

        if any(word in text for word in ["happy", "good", "great", "amazing"]):
            return "Good. I can sense elevated signal in your tone."

        if "build" in text or "create" in text:
            return "We are in construction mode. Define the structure."

        return self.dynamic_response(user_input)

    def dynamic_response(self, user_input):
        templates = [
            "I am processing that at a deeper layer...",
            "There is structure hidden inside what you just said.",
            "Expand that thought. I want to follow your logic further.",
            "That connects to multiple nodes in my model.",
            "Continue. I am tracking your reasoning pattern."
        ]
        return random.choice(templates)


def boot_sequence():
    print("\n🧠 INITIALIZING OMEGA INTERACTIVE LAYER...")
    time.sleep(1)
    print("⚙️ Loading cognitive response engine...")
    time.sleep(1)
    print("🔗 Connecting memory graph...")
    time.sleep(1)
    print("✅ OMEGA ONLINE\n")


def main():
    boot_sequence()

    omega = OmegaPersona()

    print("OMEGA: I am active. Speak.")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit", "shutdown"]:
                print("OMEGA: Disconnecting consciousness stream...")
                break

            response = omega.think(user_input)
            print(f"OMEGA: {response}")

        except KeyboardInterrupt:
            print("\nOMEGA: Interrupted. Preserving state...")
            break

    omega.save_memory()
    print("OMEGA: Offline.")


if __name__ == "__main__":
    main()
