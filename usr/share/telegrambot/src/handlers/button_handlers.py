from telegram import Update
from telegram.ext import ContextTypes
from .command_handlers import start, info, sysinfo, modeminfo

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    command = query.data
    if command == 'info':
        await info(query, context)
    elif command == 'sysinfo':
        await sysinfo(query, context)
    elif command == 'modeminfo':
        await modeminfo(query, context)