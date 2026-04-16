import time
import requests

class InternetNode:
    def __init__(self):
        self.sources = [
            "https://en.wikipedia.org/wiki/Artificial_intelligence",
            "https://en.wikipedia.org/wiki/Swarm_intelligence",
            "https://en.wikipedia.org/wiki/Machine_learning",
            "https://en.wikipedia.org/wiki/Neural_network"
        ]
        self.memory = {}

    def fetch(self):
        for url in self.sources:
            try:
                r = requests.get(url, timeout=3)
                self.memory[url] = len(r.text)
            except:
                self.memory[url] = 0

    def run(self):
        while True:
            self.fetch()
            print("🌐 INTERNET MEMORY:", list(self.memory.items())[:2])
            time.sleep(10)

if __name__ == "__main__":
    InternetNode().run()
