import os
import subprocess
import time

def restart(cmd):
    print(f"🧯 Restarting: {cmd}")
    subprocess.Popen(cmd, shell=True)

def monitor(process_map):
    while True:
        for name, cmd in process_map.items():
            # simple check
            if os.system(f"pgrep -f '{name}' > /dev/null") != 0:
                restart(cmd)
        time.sleep(5)
