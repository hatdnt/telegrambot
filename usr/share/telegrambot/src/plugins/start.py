# /usr/share/telegrambot/src/plugins/start.py

from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! Use /info to get device information.')