import os

SAFE_DIR = os.path.abspath("./sandbox")

os.makedirs(SAFE_DIR, exist_ok=True)

def write_file(filename, content):
    path = os.path.join(SAFE_DIR, filename)
    with open(path, "w") as f:
        f.write(content)
    return f"written: {filename}"

def read_file(filename):
    path = os.path.join(SAFE_DIR, filename)
    if not os.path.exists(path):
        return "file not found"
    return open(path).read()

def list_files():
    return os.listdir(SAFE_DIR)
