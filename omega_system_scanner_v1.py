import os

class OmegaSystemScanner:

    def __init__(self, roots):
        self.roots = roots
        self.files = []

    def scan(self):
        for root in self.roots:
            for dirpath, _, filenames in os.walk(root):
                for f in filenames:
                    if f.endswith(".py"):
                        self.files.append(os.path.join(dirpath, f))

        return self.files


if __name__ == "__main__":
    scanner = OmegaSystemScanner([
        "/data/data/com.termux/files/home/Omega",
        "/data/data/com.termux/files/home/Omega/omega-bot"
    ])

    files = scanner.scan()

    print("🧠 OMEGA FILE MAP")
    for f in files[:50]:
        print(f)

    print(f"\nTOTAL FILES: {len(files)}")
