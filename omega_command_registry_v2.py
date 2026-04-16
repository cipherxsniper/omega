import importlib
import os
import sys
import time
import threading

# =========================
# 🧠 GLOBAL REGISTRY STATE
# =========================

COMMANDS = {}
PLUGINS_DIR = "commands"

# =========================
# 🔌 LOAD PLUGINS
# =========================

def load_plugins():
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)

    sys.path.append(os.getcwd())

    for file in os.listdir(PLUGINS_DIR):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                mod = importlib.import_module(f"{PLUGINS_DIR}.{name}")

                if hasattr(mod, "register"):
                    mod.register(COMMANDS)

                print(f"[Ω-REGISTRY] loaded plugin: {name}")

            except Exception as e:
                print(f"[Ω-REGISTRY] failed plugin {name}: {e}")


# =========================
# ⚡ COMMAND DISPATCHER
# =========================

def run_command(cmd, parts):
    if cmd in COMMANDS:
        try:
            return COMMANDS[cmd](parts)
        except Exception as e:
            print(f"[Ω-ERROR] {cmd}: {e}")
    else:
        print(f"[Ω] unknown command: {cmd}")


# =========================
# 🔁 HOT RELOAD WATCHER
# =========================

def watch_plugins():
    last = {}

    while True:
        for f in os.listdir(PLUGINS_DIR):
            path = os.path.join(PLUGINS_DIR, f)
            if not f.endswith(".py"):
                continue

            mtime = os.path.getmtime(path)

            if f not in last or last[f] != mtime:
                print(f"[Ω-RELOAD] {f}")
                try:
                    importlib.invalidate_caches()
                    name = f[:-3]
                    mod = importlib.import_module(f"{PLUGINS_DIR}.{name}")

                    if hasattr(mod, "register"):
                        mod.register(COMMANDS)

                    last[f] = mtime

                except Exception as e:
                    print(f"[Ω-RELOAD ERROR] {e}")

        time.sleep(2)


# =========================
# 🚀 BOOTSTRAP
# =========================

def start_registry():
    load_plugins()

    t = threading.Thread(target=watch_plugins, daemon=True)
    t.start()

    print("[Ω-REGISTRY] v2 online")
