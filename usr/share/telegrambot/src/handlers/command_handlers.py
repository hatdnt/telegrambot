from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..plugins.start import start as start_command
from ..plugins.info import info as info_command
from ..plugins.sysinfo import sysinfo as sysinfo_command
from ..plugins.modeminfo import modeminfo as modeminfo_command

def get_command_buttons():
    keyboard = [
        [InlineKeyboardButton("Info", callback_data='info')],
        [InlineKeyboardButton("SysInfo", callback_data='sysinfo')],
        [InlineKeyboardButton("ModemInfo", callback_data='modeminfo')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Pilih perintah:',
        reply_markup=get_command_buttons()
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await info_command(update, context)

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await sysinfo_command(update, context)

async def modeminfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await modeminfo_command(update, context)