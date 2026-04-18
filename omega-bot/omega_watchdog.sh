#!/bin/bash

while true; do
    if ! pgrep -f app.py > /dev/null; then
        echo "🧠 Brain died — restarting"
        nohup python app.py > brain.log 2>&1 &
    fi

    if ! pgrep -f bot.py > /dev/null; then
        echo "🤖 Bot died — restarting"
        nohup python bot.py > bot.log 2>&1 &
    fi

    sleep 10
done
