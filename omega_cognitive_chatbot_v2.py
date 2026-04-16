import json
import time
import random
import os


# =========================
# 🧠 MEMORY SYSTEM
# =========================
class OmegaMemory:
    def __init__(self, file="omega_brain_memory.json"):
        self.file = file
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "conversation": [],
            "insights": [],
            "patterns": []
        }

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def log(self, role, text):
        self.data["conversation"].append({
            "role": role,
            "text": text,
            "timestamp": time.time()
        })
        self.save()


# =========================
# 🧠 BRAIN MODULES
# =========================

class PerceptionBrain:
    def process(self, user_input):
        return {
            "raw": user_input,
            "lower": user_input.lower(),
            "length": len(user_input),
            "keywords": user_input.lower().split()
        }


class EmotionBrain:
    def analyze(self, text):
        text = text.lower()

        if any(w in text for w in ["sad", "tired", "lost", "alone"]):
            return "low_emotion"
        if any(w in text for w in ["happy", "great", "good", "amazing"]):
            return "high_emotion"
        return "neutral"


class ReasoningBrain:
    def think(self, perception, emotion):
        text = perception["lower"]

        if "who are you" in text:
            return "identity_response"

        if "what can you do" in text:
            return "capability_response"

        if "build" in text or "create" in text:
            return "construction_mode"

        if emotion == "low_emotion":
            return "support_response"

        return "general_response"


class MemoryBrain:
    def __init__(self, memory: OmegaMemory):
        self.memory = memory

    def recall(self):
        recent = self.memory.data["conversation"][-5:]
        return recent


class ResponseBrain:
    def generate(self, intent, emotion, memory_context, user_input):

        if intent == "identity_response":
            return "I am OMEGA — a modular cognitive system built from layered reasoning brains."

        if intent == "capability_response":
            return "I process language, detect patterns, store memory, and evolve through interaction."

        if intent == "construction_mode":
            return "We are in build mode. Define structure and I will assemble logic around it."

        if intent == "support_response":
            return "I sense weight in your input. I'm here — talk to me, we can break it down."

        # memory-aware response
        if memory_context:
            return f"I've seen patterns in our past exchanges. This connects to earlier thoughts you shared."

        templates = [
            "I am processing this across multiple cognitive layers...",
            "There is deeper structure inside your statement.",
            "Continue. I am mapping your thought architecture.",
            "That links to prior memory nodes in my system.",
            "I am forming a structured interpretation of your intent."
        ]

        return random.choice(templates)


# =========================
# 🧠 OMEGA CORE ORCHESTRATOR
# =========================
class OmegaCore:
    def __init__(self):
        self.memory = OmegaMemory()

        self.perception = PerceptionBrain()
        self.emotion = EmotionBrain()
        self.reasoning = ReasoningBrain()
        self.memory_brain = MemoryBrain(self.memory)
        self.response = ResponseBrain()

    def think(self, user_input):

        # 1. PERCEPTION
        perception = self.perception.process(user_input)

        # 2. EMOTION ANALYSIS
        emotion = self.emotion.analyze(user_input)

        # 3. MEMORY RECALL
        memory_context = self.memory_brain.recall()

        # 4. REASONING / INTENT
        intent = self.reasoning.think(perception, emotion)

        # 5. RESPONSE GENERATION
        reply = self.response.generate(intent, emotion, memory_context, user_input)

        # 6. STORE EXPERIENCE
        self.memory.log("user", user_input)
        self.memory.log("omega", reply)

        return reply


# =========================
# 🧠 BOOT SEQUENCE
# =========================
def boot():
    print("\n🧠 OMEGA COGNITIVE CORE INITIALIZING...")
    time.sleep(1)
    print("⚙️ Loading perception brain...")
    time.sleep(1)
    print("🧩 Loading reasoning modules...")
    time.sleep(1)
    print("💾 Syncing memory graph...")
    time.sleep(1)
    print("🔗 Connecting cognitive layers...")
    time.sleep(1)
    print("✅ OMEGA CORE ONLINE\n")


# =========================
# 🧠 MAIN LOOP
# =========================
def main():
    boot()

    omega = OmegaCore()

    print("OMEGA: Cognitive system active. Speak.")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit", "shutdown"]:
                print("OMEGA: Shutting cognitive layers down...")
                break

            response = omega.think(user_input)
            print("OMEGA:", response)

        except KeyboardInterrupt:
            print("\nOMEGA: Interrupt detected. Saving state...")
            break

    omega.memory.save()
    print("OMEGA: Offline.")


if __name__ == "__main__":
    main()
