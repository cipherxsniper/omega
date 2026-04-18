import os

def scan_files(root):
    py_files = []
    for r, d, f in os.walk(root):
        for file in f:
            if file.endswith(".py"):
                py_files.append(os.path.join(r, file))
    return py_files
