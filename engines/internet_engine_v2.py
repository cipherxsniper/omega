# engines/internet_engine_v2.py

import requests

class InternetEngine:
    def ingest(self):
        try:
            fact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()["text"]
            return {"fact": fact}
        except:
            return {"fact": "fallback"}

