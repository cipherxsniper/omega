# OMEGA EVENT STORE v2
# Persistent system memory log

import json
from pathlib import Path

DB = Path("omega_events.jsonl")


def log_event(event):
    with open(DB, "a") as f:
        f.write(json.dumps(event) + "\n")


def load_events(limit=100):
    if not DB.exists():
        return []

    with open(DB) as f:
        return f.readlines()[-limit:]
