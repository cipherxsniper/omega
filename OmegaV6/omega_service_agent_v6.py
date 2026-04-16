import time
import sys

service = sys.argv[1]

while True:
    # simulate heartbeat workload
    time.sleep(2)
