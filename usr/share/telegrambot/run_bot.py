# /usr/share/telegrambot/run_bot.py

import asyncio
from src.bot import main

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Jika event loop sudah berjalan, jalankan main di dalamnya
            asyncio.ensure_future(main())
        else:
            # Jika event loop belum berjalan, jalankan main dengan run_until_complete
            loop.run_until_complete(main())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(main())
            loop.run_forever()
        else:
            raise