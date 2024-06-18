import logging
from telegram import Update, InputFile
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

logger = logging.getLogger(__name__)

# Definisikan state untuk ConversationHandler
WAITING_FOR_PATH = 1

async def start_download(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Silakan kirim path file yang ingin diunduh dari OpenWRT.")
    return WAITING_FOR_PATH

async def handle_path_input(update: Update, context: CallbackContext) -> int:
    file_path = update.message.text
    try:
        with open(file_path, 'rb') as f:
            await update.message.reply_document(document=InputFile(f), filename=file_path.split('/')[-1])
        await update.message.reply_text(f"File berhasil diunduh dari {file_path}.")
    except Exception as e:
        logger.error(f"Error saat mengunduh file: {e}")
        await update.message.reply_text(f"Gagal mengunduh file: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Proses unduh dibatalkan.")
    return ConversationHandler.END

# Buat ConversationHandler untuk mengelola percakapan
download_handler = ConversationHandler(
    entry_points=[CommandHandler('download', start_download)],
    states={
        WAITING_FOR_PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_path_input)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)