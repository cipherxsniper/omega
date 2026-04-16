#!/usr/bin/env python3

import os
import sys
sys.path.append(os.getcwd())

import time
import json
import random
import importlib
from datetime import datetime
from collections import deque, defaultdict

# 🧠 MEMORY CORE
from omega_memorycore_v1 import start as memory_start, inject_into_module, write as memory_write

memory_start()

# ---------------- CONFIG ----------------

LOG_FILE = "mega_logs/learning_engine_v17.log"
MEMORY_SIZE = 5000
SLEEP_INTERVAL = 1
PATTERN_THRESHOLD = 3
SIMULATION_COUNT = 5
SNAPSHOT_INTERVAL = 300

# ---------------- STATE ----------------

memory_local = deque(maxlen=MEMORY_SIZE)
node_weights = defaultdict(lambda: 1.0)
last_actions = deque(maxlen=200)
last_snapshot = time.time()
error_count = 0

NODE_INPUT_PATHS = []

# ---------------- AUTO IMPORT ALL PY FILES ----------------

def discover_modules():
    modules = []
    for file in os.listdir():
        if file.endswith(".py") and file not in ["learning_engine_v17.py", "omega_memorycore_v1.py"]:
            modules.append(file.replace(".py", ""))
    return modules

def dynamic_import(modules):
    imported = {}
    for mod in modules:
        try:
            module = importlib.import_module(mod)
            imported[mod] = module
            NODE_INPUT_PATHS.append(f"mega_logs/{mod}_forever.log")

            # 🧠 Inject shared memory
            inject_into_module(module)

            log(f"[IMPORT] {mod}")
        except Exception as e:
            log(f"[IMPORT ERROR] {mod}: {e}")
            memory_write(str(e), source=mod, mtype="error", importance=2.0)

    return imported

# ---------------- LOGGING ----------------

def log(msg, confidence=None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conf = f" [CONF:{confidence:.2f}]" if confidence else ""
    line = f"[LEARNING_V17 {ts}]{conf} {msg}"

    print(line)

    os.makedirs("mega_logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ---------------- EVENT INGEST ----------------

def read_logs():
    events = []
    for path in NODE_INPUT_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    lines = f.readlines()[-20:]
                    for line in lines:
                        if line.strip():
                            events.append({"node": path, "event": line.strip()})
            except:
                continue
    return events

# ---------------- ANALYSIS ----------------

def analyze(events):
    global error_count
    insights = []

    for e in events:
        text = e["event"].lower()

        if "traceback" in text or "error" in text:
            error_count += 1
            insights.append({"type": "error", **e})

        elif "prediction" in text:
            insights.append({"type": "prediction", **e})

        elif "decision" in text:
            insights.append({"type": "decision", **e})

        elif "feedback" in text:
            insights.append({"type": "feedback", **e})

        else:
            insights.append({"type": "misc", **e})

    return insights

# ---------------- LEARNING ----------------

def learn(insights):
    for i in insights:
        memory_local.append(i)

        count = sum(1 for m in memory_local if m["event"] == i["event"])

        if count >= PATTERN_THRESHOLD and i["type"] != "error":
            log(f"[PATTERN] {i['event']} x{count}")
            memory_write(i["event"], source=i["node"], mtype="pattern", importance=2.0)

# ---------------- WEIGHTING ----------------

def update_weights(insights):
    for i in insights:
        node_weights[i["node"]] += 0.05

    for n in node_weights:
        node_weights[n] *= 0.995
        node_weights[n] = max(node_weights[n], 0.1)

# ---------------- SIMULATION ----------------

def simulate(insights):
    predictions = []

    for _ in range(SIMULATION_COUNT):
        if not insights:
            continue

        sample = random.sample(insights, min(len(insights), 3))
        confidence = sum(node_weights[i["node"]] for i in sample) / len(sample)

        predictions.append({
            "scenario": sample,
            "confidence": confidence
        })

    return predictions

# ---------------- ACTION ----------------

def act(predictions):
    for p in predictions:
        scenario = " | ".join(i["event"] for i in p["scenario"])

        if scenario in last_actions:
            continue

        last_actions.append(scenario)

        log(f"[ACTION] {scenario}", p["confidence"])

        for e in p["scenario"]:
            if e["type"] == "error":
                log(f"[IMMUNE] Ignoring error pattern: {e['event']}")
                continue

            memory_write(e["event"], source=e["node"], mtype=e["type"], importance=p["confidence"])

# ---------------- SELF CORRECTION ----------------

def self_correct(insights):
    for i in insights:
        if i["type"] == "error":
            if "intent_logs" in i["event"]:
                log("[FIX] IntentEngine missing intent_logs → patch suggested")

            if "memory" in i["event"]:
                log("[FIX] Memory corruption detected → reset suggested")

# ---------------- DASHBOARD ----------------

def dashboard():
    data = {
        "time": datetime.now().isoformat(),
        "memory_size": len(memory_local),
        "nodes": dict(node_weights),
        "health": max(0, 100 - error_count)
    }

    with open("mega_logs/dashboard_v17.json", "w") as f:
        json.dump(data, f, indent=2)

# ---------------- MAIN ----------------

def main():
    log("🚀 OMEGA v17 ONLINE")

    modules = discover_modules()
    imported = dynamic_import(modules)

    while True:
        try:
            events = read_logs()

            if events:
                insights = analyze(events)

                learn(insights)
                update_weights(insights)

                predictions = simulate(insights)
                act(predictions)

                self_correct(insights)
                dashboard()

            else:
                log("No events...")

        except Exception as e:
            log(f"[CRASH] {e}")
            memory_write(str(e), source="engine", mtype="error", importance=3.0)

        time.sleep(SLEEP_INTERVAL)

# ---------------- RUN ----------------

if __name__ == "__main__":
    main()
