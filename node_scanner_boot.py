import os
import importlib.util

OMEGA_ROOTS = [
    "/data/data/com.termux/files/home/Omega",
    "/data/data/com.termux/files/home/Omega/omega-bot"
]

nodes = {}

def load_py(path):
    name = os.path.basename(path).replace(".py","")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        nodes[name] = mod
    except Exception as e:
        nodes[name] = str(e)

def scan():
    for root in OMEGA_ROOTS:
        for r, d, f in os.walk(root):
            for file in f:
                if file.endswith(".py") and "venv" not in r:
                    load_py(os.path.join(r, file))

if __name__ == "__main__":
    scan()
    print(f"🧠 Nodes loaded: {len(nodes)}")
