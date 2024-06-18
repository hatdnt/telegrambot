import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from .config import BOT_TOKEN
from .handlers.line_limit_file_handler import LineLimitFileHandler  # Impor dari file baru
from .plugins.start import start
from .plugins.info import info
from .plugins.sysinfo import sysinfo
from .plugins.modeminfo import modeminfo
from .plugins.vnstat import vnstat
from .plugins.proxies import proxies
from .plugins.upload import upload_handler
from .plugins.download import download_handler

def main() -> None:
    # Konfigurasi logging
    log_filename = '/usr/share/telegrambot/logs/bot.log'
    log_handler = LineLimitFileHandler(log_filename, max_lines=300, mode='a', encoding='utf-8')
    logging.basicConfig(
        level=logging.INFO,
        handlers=[log_handler],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    logger.info("Memulai bot...")

    # Buat Aplikasi dan berikan token bot Anda.
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # pada perintah yang berbeda - jawab di Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("sysinfo", sysinfo))
    application.add_handler(CommandHandler("modeminfo", modeminfo))
    application.add_handler(CommandHandler("vnstat", vnstat))
    application.add_handler(CommandHandler("proxies", proxies))
    application.add_handler(upload_handler)
    application.add_handler(download_handler)

    # Jalankan bot dengan polling
    logger.info("Bot sedang berjalan. Tekan Ctrl+C untuk menghentikan.")
    application.run_polling()

if __name__ == '__main__':
    main()