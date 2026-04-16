import requests
import time
from collections import defaultdict, Counter
import math

# -----------------------------
# 🌐 INTERNET KNOWLEDGE SOURCES
# -----------------------------
SOURCES = {
    "wiki": "https://en.wikipedia.org/wiki/",
    "stack": "https://stackoverflow.com/questions/tagged/",
    "arxiv": "https://arxiv.org/search/?query=",
    "nature": "https://www.nature.com/search?q=",
    "mit": "https://news.mit.edu/search/advanced?search_api_fulltext=",
    "nasa": "https://www.nasa.gov/search/?q=",
    "reddit": "https://www.reddit.com/search/?q=",
    "github": "https://github.com/search?q=",
    "towardsai": "https://towardsdatascience.com/search?q=",
    "deepmind": "https://deepmind.google/discover/blog/"
}

# -----------------------------
# 🧠 SEMANTIC COGNITION ENGINE
# -----------------------------
class OmegaMeshV10SemanticCognition:

    def __init__(self):
        self.memory = defaultdict(float)     # semantic concept weights
        self.history = []                    # raw knowledge stream
        self.tick = 0

    # -----------------------------
    # 🌐 INTERNET QUERY (SIMULATED SAFE FETCH)
    # -----------------------------
    def query_internet(self, query):
        """
        Simulated multi-source extraction layer
        (replace with real scraping or APIs later)
        """
        results = {}

        for name, base in SOURCES.items():
            results[name] = f"{base}{query.replace(' ', '+')}"

        return results

    # -----------------------------
    # 🧠 SEMANTIC PARSER (FIXES YOUR ISSUE)
    # -----------------------------
    def semantic_parse(self, text):
        """
        Instead of splitting words → we build concept chunks
        """
        words = text.lower().split()

        concepts = []
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            concepts.append(pair)

        # add full phrase compression
        concepts.append(text.lower())

        return concepts

    # -----------------------------
    # 🔁 MEMORY UPDATE (LEARNING LOOP)
    # -----------------------------
    def update_memory(self, concepts):
        for c in concepts:
            self.memory[c] += 1.0

    # -----------------------------
    # 📊 CONCEPT NORMALIZATION
    # -----------------------------
    def normalize_memory(self):
        total = sum(self.memory.values()) + 1e-9

        normalized = {
            k: v / total for k, v in self.memory.items()
        }

        return dict(sorted(normalized.items(), key=lambda x: x[1], reverse=True))

    # -----------------------------
    # 🧠 COGNITIVE STEP
    # -----------------------------
    def step(self, query):
        self.tick += 1

        # 1. fetch knowledge
        internet = self.query_internet(query)

        # 2. extract semantic concepts
        concepts = self.semantic_parse(query)

        # 3. store experience
        self.history.append({
            "tick": self.tick,
            "query": query,
            "sources": internet,
            "concepts": concepts
        })

        # 4. update memory
        self.update_memory(concepts)

        # 5. normalize cognition state
        state = self.normalize_memory()

        return state

    # -----------------------------
    # 🧠 INSIGHT ENGINE
    # -----------------------------
    def top_concepts(self, n=10):
        return list(self.normalize_memory().items())[:n]


# -----------------------------
# 🚀 RUN SYSTEM
# -----------------------------
if __name__ == "__main__":
    brain = OmegaMeshV10SemanticCognition()

    queries = [
        "what is utility theory in artificial intelligence",
        "how do neural networks learn patterns",
        "what is swarm intelligence in distributed systems",
        "how does reinforcement learning work",
        "what is emergence in complex systems"
    ]

    for q in queries:
        state = brain.step(q)
        print("\n🧠 STATE UPDATE:")
        print(state)

        print("\n🔥 TOP CONCEPTS:")
        print(brain.top_concepts(5))
        time.sleep(0.5)
