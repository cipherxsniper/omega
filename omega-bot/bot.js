import 'dotenv/config';
import { Telegraf } from 'telegraf';
import { askOmega } from './brain.js';

const bot = new Telegraf(process.env.TELEGRAM_TOKEN);

bot.start((ctx) => {
  ctx.reply("🧠 Omega Mind Online");
});

bot.on('text', async (ctx) => {
  const userId = ctx.from.id.toString();
  const msg = ctx.message.text;

  try {
    const reply = await askOmega(userId, msg);
    ctx.reply(reply);
  } catch (err) {
    console.error(err);
    ctx.reply("Omega error.");
  }
});

bot.launch();
console.log("🧠 Omega Running...");
