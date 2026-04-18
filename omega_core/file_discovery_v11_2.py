# 📡 Omega v11.2 CLEAN FILE DISCOVERY (FILTERED)

import os

ALLOWED_PREFIXES = (
    "omega",
    "Omega",
    "node_",
    "core_"
)

BLOCKED_PATTERNS = (
    "_httpx",
    "_request",
    "_urllib",
    "_async",
    "site-packages"
)

class FileDiscovery:

    def __init__(self):
        self.known = set()

    def valid(self, path):

        name = os.path.basename(path)

        # block noise
        for b in BLOCKED_PATTERNS:
            if b in name:
                return False

        # allow only omega ecosystem
        return name.startswith(ALLOWED_PREFIXES)

    def scan(self, root="~/Omega"):

        root = os.path.expanduser(root)

        new_files = []

        for r, d, f in os.walk(root):
            for file in f:

                if not file.endswith(".py"):
                    continue

                full = os.path.join(r, file)

                if not self.valid(full):
                    continue

                if full not in self.known:
                    self.known.add(full)
                    new_files.append(file.replace(".py",""))

        return new_files
