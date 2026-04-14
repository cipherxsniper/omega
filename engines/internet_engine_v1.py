# engines/internet_engine_v1.py (UPGRADE)

import requests

class InternetEngine:
    def ingest(self):
        try:
            fact = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()["text"]

            # ❌ Reject garbage
            if len(fact) < 20:
                return self.ingest()

            return {
                "crypto": None,
                "fact": fact
            }

        except:
            return {
                "crypto": None,
                "fact": "fallback_data"
            }
