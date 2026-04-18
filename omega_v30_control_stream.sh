#!/bin/bash

tail -f logs/brain.log logs/watchdog.log logs/node_auto.log logs/mesh_view.log \
| awk '!seen[$0]++' \
| grep --line-buffered -E "SWARM|Active|AVG|tick|leader|node|MESH|heartbeat"
