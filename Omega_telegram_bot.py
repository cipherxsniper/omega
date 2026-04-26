
import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================

load_dotenv()

TOKEN = os.getenv("OMEGA_TELEGRAM_TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN")

BASE = f"https://api.telegram.org/bot{TOKEN}"
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

offset = 0

# =========================
# IN-MEMORY EVENT PIPE
# =========================

queue = asyncio.Queue()

# =========================
# TELEGRAM CLIENT (ASYNC)
# =========================

async def tg_get(session):
    global offset
    url = BASE + "/getUpdates"

    async with session.get(url, params={"timeout": 1, "offset": offset}) as r:
        data = await r.json()

        for u in data.get("result", []):
            offset = u["update_id"] + 1
            msg = u.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")

            if text:
                await queue.put((chat_id, text))

async def tg_send(session, chat_id, text):
    async with session.post(
        BASE + "/sendMessage",
        data={"chat_id": chat_id, "text": text}
    ) as r:
        data = await r.json()
        return data["result"]["message_id"]

async def tg_edit(session, chat_id, msg_id, text):
    try:
        await session.post(
            BASE + "/editMessageText",
            data={
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": text
            }
        )
    except:
        pass

# =========================
# OLLAMA STREAM (TRUE PIPE)
# =========================

async def ollama_stream(session, prompt):
    async with session.post(
        OLLAMA,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True
        }
    ) as resp:

        async for line in resp.content:
            try:
                if not line:
                    continue
                data = json.loads(line.decode())
                token = data.get("response", "")
                if token:
                    yield token
            except:
                continue

# =========================
# PROCESSOR (ZERO BLOCKING)
# =========================

async def handle(session, chat_id, text):
    msg_id = await tg_send(session, chat_id, "🧠")

    buffer = ""
    count = 0

    async for token in ollama_stream(session, text):
        buffer += token
        count += 1

        # ultra low latency batching
        if count % 2 == 0:
            await tg_edit(session, chat_id, msg_id, "🧠 " + buffer)

    await tg_edit(session, chat_id, msg_id, "🧠 " + buffer)

# =========================
# WORKER LOOP
# =========================

async def worker(session):
    while True:
        chat_id, text = await queue.get()
        await handle(session, chat_id, text)

# =========================
# POLL LOOP (FAST EVENT FEED)
# =========================

async def poller(session):
    while True:
        await tg_get(session)
        await asyncio.sleep(0.2)

# =========================
# MAIN
# =========================

async def main():
    print("🧠 Omega ZERO-LATENCY Kernel ONLINE")

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            poller(session),
            worker(session),
            worker(session)
        )

asyncio.run(main())
