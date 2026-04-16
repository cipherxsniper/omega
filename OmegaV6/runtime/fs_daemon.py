import time
import os

WATCH_DIR = os.environ.get("OMEGA_ROOT", ".")

def scan():
    return os.listdir(WATCH_DIR)

def main():
    print("[FS-DAEMON] Omega file system watcher active")

    while True:
        files = scan()
        print("[FS-DAEMON] files:", len(files))
        time.sleep(2)

if __name__ == "__main__":
    main()
