import logging
import subprocess
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
BOT_TOKEN = "<TOKEN>"

from llm import generate
tok, model = None, None

import json
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def gpt_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    generated = generate.generate(model, tok, update.message.text, num_beams=3)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=generated[0])

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    print("downloading models...")
    tok, model = generate.load_tokenizer_and_model("ai-forever/rugpt3large_based_on_gpt2")
    
    start_handler = CommandHandler('start', start)
    gpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_reply)

    application.add_handler(start_handler)
    application.add_handler(gpt_handler)

    application.run_polling()