pkill -f app.py
pkill -f bot.py

echo "🧠 Starting Omega v23 Autonomous System..."

nohup python app.py > brain.log 2>&1 &
nohup python bot.py > bot.log 2>&1 &

echo "✅ Omega v23 ONLINE: planning + reasoning + tools"
