#!/usr/bin/env python3

import subprocess
import threading
import queue
import re
import json
from datetime import datetime

def emit(queue_bus, source, line):
    msg = {
        "time": datetime.utcnow().isoformat(),
        "source": source,
        "type": "log",
        "data": line.strip()
    }
    queue_bus.put(msg)

def run_node(script, bus):
    proc = subprocess.Popen(
        ["python3", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in proc.stdout:
        # BASIC INTELLIGENCE PARSING
        if re.match(r'^[01\s]+$', line.strip()) and len(line.strip()) > 16:
            emit(bus, script, "[BINARY_STREAM_DETECTED] " + line.strip())
        else:
            emit(bus, script, line)

def start_node(script, bus):
    t = threading.Thread(target=run_node, args=(script, bus), daemon=True)
    t.start()
    return t
