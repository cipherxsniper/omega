#!/bin/bash

tail -f logs/brain.log logs/watchdog.log logs/control.log 2>/dev/null \
| grep --line-buffered -E "CONSENSUS|STABILITY|NODES|tick|error|weight"
