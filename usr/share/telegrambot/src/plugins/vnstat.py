import subprocess
import json
from telegram import Update
from telegram.ext import CallbackContext

async def vnstat(update: Update, context: CallbackContext) -> None:
    try:
        # Jalankan perintah vnstat dengan opsi --json dan ambil outputnya
        result = subprocess.run(['vnstat', '--json'], capture_output=True, text=True)
        output = result.stdout

        # Parse JSON output
        data = json.loads(output)

        # Ambil informasi yang diperlukan
        interfaces = data['interfaces']
        formatted_output = ""

        for interface in interfaces:
            name = interface['name']
            today_rx = interface['traffic']['day'][0]['rx']
            today_tx = interface['traffic']['day'][0]['tx']
            today_total = today_rx + today_tx
            
            total_rx = interface['traffic']['total']['rx']
            total_tx = interface['traffic']['total']['tx']
            total = total_rx + total_tx

            formatted_output += f"{name}:\n"
            formatted_output += f"  Today:\n"
            formatted_output += f"    RX: {today_rx / (1024**3):.2f} GiB\n"
            formatted_output += f"    TX: {today_tx / (1024**3):.2f} GiB\n"
            formatted_output += f"    Total: {today_total / (1024**3):.2f} GiB\n\n"
            formatted_output += f"  All time:\n"
            formatted_output += f"    RX: {total_rx / (1024**3):.2f} GiB\n"
            formatted_output += f"    TX: {total_tx / (1024**3):.2f} GiB\n"
            formatted_output += f"    Total: {total / (1024**3):.2f} GiB\n"

        # Kirim output yang diformat ke pengguna
        await update.message.reply_text(f"```\n{formatted_output}\n```", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {e}")