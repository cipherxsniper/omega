#!/bin/bash

tail -F logs/brain.log logs/control.log logs/watchdog.log logs/node_auto.log | grep --line-buffered -E "SWARM|Active|AVG|node|tick|MESH|HIGH|watchdog|heartbeat"
