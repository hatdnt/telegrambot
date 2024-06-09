# /usr/share/telegrambot/src/plugins/sysinfo.py

import subprocess
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Dapatkan informasi mesin
    try:
        machine_info = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        machine_info = f"Error retrieving machine info: {e}"
    
    # Dapatkan informasi uptime
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            uptime_info = f"{hours} jam, {minutes} menit, {seconds} detik"
    except Exception as e:
        uptime_info = f"Error retrieving uptime: {e}"
    
    # Dapatkan informasi suhu (asumsi suhu tersedia di /sys/class/thermal/thermal_zone0/temp)
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_info = f"{float(f.readline().strip()) / 1000.0}°C"
    except FileNotFoundError:
        temp_info = "Temperature information not available"
    except Exception as e:
        temp_info = f"Error retrieving temperature: {e}"
        
        # Dapatkan waktu saat ini menggunakan perintah date
    try:
        current_time = subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        current_time = f"Error retrieving current time: {e}"
    
    # Format informasi sistem
    sys_info = (
        f"Uptime: {uptime_info}\n"
        f"Now: {current_time}\n"
        f"Temperature: {temp_info}"
    )
    
    # Kirim informasi sistem kembali ke pengguna
    await update.message.reply_text(f'System Information\n\n{sys_info}')