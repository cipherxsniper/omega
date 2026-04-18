import os
import time

WATCH_PATHS = ["~/Omega"]

class DiscoveryEngine:

    def __init__(self):
        self.known = set()

    def scan(self):
        found = []

        for path in WATCH_PATHS:
            path = os.path.expanduser(path)

            for root, dirs, files in os.walk(path):
                for f in files:

                    if not f.endswith(".py"):
                        continue

                    full = os.path.join(root, f)

                    if full not in self.known:
                        self.known.add(full)
                        found.append(full)

        return found
