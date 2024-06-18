import logging
import os
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters

logger = logging.getLogger(__name__)

# Definisikan state untuk ConversationHandler
WAITING_FOR_FILE = 1
WAITING_FOR_PATH = 2

async def start_upload(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Silakan kirim file yang ingin diunggah.")
    return WAITING_FOR_FILE

async def handle_file_upload(update: Update, context: CallbackContext) -> int:
    file = update.message.document
    if not file:
        await update.message.reply_text("Tidak ada file yang terdeteksi. Silakan kirim file yang valid.")
        return WAITING_FOR_FILE

    context.user_data['file'] = file
    await update.message.reply_text("File diterima. Silakan masukkan path direktori penyimpanan.")
    return WAITING_FOR_PATH

async def handle_path_input(update: Update, context: CallbackContext) -> int:
    file = context.user_data.get('file')
    if not file:
        await update.message.reply_text("Terjadi kesalahan. Silakan mulai ulang proses dengan /upload.")
        return ConversationHandler.END

    directory_path = update.message.text

    # Periksa apakah path yang diberikan adalah direktori
    if not os.path.isdir(directory_path):
        await update.message.reply_text("Path yang diberikan bukan direktori. Silakan masukkan path direktori yang valid.")
        return WAITING_FOR_PATH

    try:
        await update.message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        file_info = await file.get_file()
        file_path = os.path.join(directory_path, file.file_name)
        await file_info.download_to_drive(file_path)
        await update.message.reply_text(f"File {file.file_name} berhasil diunggah ke {file_path}.")
    except Exception as e:
        logger.error(f"Error saat mengunggah file: {e}")
        await update.message.reply_text(f"Gagal mengunggah file: {e}")

    # Reset state setelah selesai
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Proses unggah dibatalkan.")
    context.user_data.clear()
    return ConversationHandler.END

# Buat ConversationHandler untuk mengelola percakapan
upload_handler = ConversationHandler(
    entry_points=[CommandHandler('upload', start_upload)],
    states={
        WAITING_FOR_FILE: [MessageHandler(filters.Document.ALL, handle_file_upload)],
        WAITING_FOR_PATH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_path_input)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)