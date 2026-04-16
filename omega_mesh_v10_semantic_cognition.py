import requests
import time
import re
from collections import defaultdict

# ==============================
# 🧠 STOPWORDS (lightweight set)
# ==============================
STOPWORDS = set([
    "the","is","in","at","of","and","a","to","for","on","what","how",
    "this","that","it","as","with","by","an","be","are","from"
])

# ==============================
# 🧠 CLEANING ENGINE
# ==============================
class TextCleaner:
    @staticmethod
    def clean(text: str):
        text = text.lower()
        text = re.sub(r"&#\d+;|&\w+;", "", text)   # html entities
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        words = text.split()
        words = [w for w in words if w not in STOPWORDS]
        return words

    @staticmethod
    def extract_concepts(words):
        """
        Turns word stream into concept-like 2–3 word phrases
        """
        concepts = []

        for i in range(len(words) - 1):
            pair = words[i] + " " + words[i+1]
            concepts.append(pair)

        for i in range(len(words) - 2):
            tri = words[i] + " " + words[i+1] + " " + words[i+2]
            concepts.append(tri)

        return concepts[:30]

# ==============================
# 🌐 INTERNET LAYER
# ==============================
class InternetLayer:
    def fetch_wiki(self, query):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json().get("extract", "")
        return ""

    def fetch_stack(self, query):
        url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
        r = requests.get(url)
        if r.status_code == 200:
            items = r.json().get("items", [])
            if items:
                return items[0].get("title", "")
        return ""

# ==============================
# 🧠 SEMANTIC BRAIN (V10 CORE)
# ==============================
class SemanticBrain:
    def __init__(self):
        self.concept_graph = defaultdict(float)
        self.source_map = defaultdict(list)

    def ingest(self, text, source, weight=1.0):
        words = TextCleaner.clean(text)
        concepts = TextCleaner.extract_concepts(words)

        for c in concepts:
            self.concept_graph[c] += weight
            self.source_map[c].append(source)

    def top_concepts(self, n=10):
        return sorted(self.concept_graph.items(), key=lambda x: x[1], reverse=True)[:n]

# ==============================
# 🌐 OMEGA V10 SYSTEM
# ==============================
class OmegaV10:
    def __init__(self):
        self.internet = InternetLayer()
        self.brain = SemanticBrain()

    def run_cycle(self, query):
        print("\n🌐 Querying internet...\n")

        wiki = self.internet.fetch_wiki(query)
        stack = self.internet.fetch_stack(query)

        if wiki:
            self.brain.ingest(wiki, "wikipedia", weight=0.9)

        if stack:
            self.brain.ingest(stack, "stackexchange", weight=0.6)

        print("\n🧠 TOP CONCEPTS:\n")
        for c, w in self.brain.top_concepts(10):
            print(f"{c} → {round(w,3)}")

# ==============================
# 🚀 RUN
# ==============================
if __name__ == "__main__":
    omega = OmegaV10()
    omega.run_cycle("artificial intelligence")
