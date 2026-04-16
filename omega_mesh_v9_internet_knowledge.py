import requests
import time
from collections import defaultdict

# ==============================
# 🌐 INTERNET KNOWLEDGE LAYER
# ==============================
class InternetKnowledgeLayer:
    def __init__(self):
        self.cache = {}
        self.beliefs = defaultdict(float)

        self.sources = {
            "wikipedia": 0.7,
            "wikidata": 0.8,
            "arxiv": 0.85,
            "pubmed": 0.9,
            "nasa": 0.95,
            "noaa": 0.9,
            "open_meteo": 0.75,
            "github": 0.7,
            "stackexchange": 0.6,
            "openalex": 0.85
        }

    # ------------------------------
    # WIKIPEDIA FETCH (SAFE API)
    # ------------------------------
    def wiki(self, query):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json().get("extract", "")
        return ""

    # ------------------------------
    # NASA API (example endpoint)
    # ------------------------------
    def nasa(self):
        url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        r = requests.get(url)
        if r.status_code == 200:
            return r.json().get("explanation", "")
        return ""

    # ------------------------------
    # STACKEXCHANGE (knowledge Q&A)
    # ------------------------------
    def stack(self, query):
        url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow"
        r = requests.get(url)
        if r.status_code == 200:
            items = r.json().get("items", [])
            if items:
                return items[0].get("title", "")
        return ""

    # ------------------------------
    # INGEST INTO SWARM BELIEF FIELD
    # ------------------------------
    def ingest(self, source, text):
        weight = self.sources.get(source, 0.5)
        tokens = text.split()[:20]

        for t in tokens:
            self.beliefs[t.lower()] += weight

    # ------------------------------
    # QUERY PIPELINE
    # ------------------------------
    def query_all(self, query):
        data = {}

        w = self.wiki(query)
        self.ingest("wikipedia", w)
        data["wiki"] = w

        s = self.stack(query)
        self.ingest("stackexchange", s)
        data["stack"] = s

        n = self.nasa()
        self.ingest("nasa", n)
        data["nasa"] = n

        return data

    # ------------------------------
    # TOP KNOWLEDGE
    # ------------------------------
    def top_beliefs(self, n=10):
        return sorted(self.beliefs.items(), key=lambda x: x[1], reverse=True)[:n]


# ==============================
# 🚀 DEMO RUN
# ==============================
if __name__ == "__main__":
    ikl = InternetKnowledgeLayer()

    print("Querying internet knowledge sources...\n")

    result = ikl.query_all("artificial intelligence")

    print("\n--- SAMPLE OUTPUT ---")
    for k, v in result.items():
        print(f"\n[{k.upper()}]\n{v[:200]}")

    print("\n--- TOP BELIEFS ---")
    print(ikl.top_beliefs())
