#!/bin/bash

tail -f logs/brain.log logs/watchdog.log logs/control.log 2>/dev/null \
| awk '!seen[$0]++' \
| grep --line-buffered -E "CONSENSUS|STABILITY|NODE|TICK|ACTIVE|deficit|Mesh"
