import importlib.util
import os
import time

PLUGIN_DIR = "./plugins"
LOADED = {}

# ---------------------------
# LOAD PLUGIN
# ---------------------------

def load_plugin(path):
    name = os.path.basename(path).replace(".py", "")

    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    LOADED[name] = mod

# ---------------------------
# SCAN PLUGINS
# ---------------------------

def scan():
    for f in os.listdir(PLUGIN_DIR):
        if f.endswith(".py"):
            load_plugin(os.path.join(PLUGIN_DIR, f))

# ---------------------------
# LOOP
# ---------------------------

def run():
    while True:
        scan()
        time.sleep(5)

if __name__ == "__main__":
    run()
