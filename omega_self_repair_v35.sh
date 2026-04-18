#!/bin/bash

echo "🧠 Omega Self Repair Engine Active"

# detect crashed python processes
ps aux | grep python | awk '{print $2}' > running_nodes.txt

# restart core if missing
if ! pgrep -f omega_message_bus; then
    echo "repair: message bus restart"
    nohup python omega_message_bus_v72.py &
fi

if ! pgrep -f memory_core; then
    echo "repair: memory core restart"
    nohup python memory_core.py &
fi

if ! pgrep -f app.py; then
    echo "repair: app restart"
    nohup python app.py &
fi

echo "🧠 Repair cycle complete"
