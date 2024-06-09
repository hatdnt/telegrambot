# /usr/share/telegrambot/src/plugins/info.py

import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Run a shell command to get device information
    result = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE)
    device_info = result.stdout.decode('utf-8')
    
    # Send the device information back to the user
    await update.message.reply_text(f'Device Information:\n{device_info}')