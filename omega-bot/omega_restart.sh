pkill -f app.py
pkill -f bot.py

echo "🧠 restarting Omega + GPT4All hybrid system..."

nohup python app.py > brain.log 2>&1 &
nohup python bot.py > bot.log 2>&1 &

echo "✅ Omega fully online (LLM + swarm + memory)"
