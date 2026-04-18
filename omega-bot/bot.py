import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
BRAIN_URL = "http://127.0.0.1:5000/chat"

def ask_brain(user_id, message):
    try:
        r = requests.post(
            BRAIN_URL,
            json={"user_id": user_id, "message": message},
            timeout=5
        )

        # 🧠 SAFE PARSE (NO CRASH EVER)
        try:
            data = r.json()
            return data.get("reply", "⚠️ no reply field")
        except:
            return f"⚠️ brain returned non-json: {r.text[:100]}"

    except Exception as e:
        return f"⚠️ Omega unreachable: {str(e)}"

async def handle(update, context):
    user_id = str(update.message.from_user.id)
    msg = update.message.text

    reply = ask_brain(user_id, msg)

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🤖 Omega SAFE MODE BOT ONLINE")
    app.run_polling()

if __name__ == "__main__":
    main()
