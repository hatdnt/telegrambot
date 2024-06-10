import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def modeminfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Dapatkan informasi protokol dari ModemManager menggunakan mmcli
    try:
        mmcli_output = subprocess.run(['mmcli', '-m', '8'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        protocol = None
        uptime = None
        for line in mmcli_output.split('\n'):
            if 'access tech' in line:
                protocol = line.split(':')[-1].strip()
            if 'state' in line and 'connected' in line:
                uptime = line.split('connected since')[-1].strip()
        if protocol is None:
            protocol = "Protocol information not available"
        if uptime is None:
            uptime = "Uptime information not available"
    except subprocess.CalledProcessError as e:
        protocol = f"Error retrieving protocol info: {e}"
        uptime = f"Error retrieving uptime info: {e}"
    except FileNotFoundError as e:
        protocol = f"mmcli command not found: {e}"
        uptime = f"mmcli command not found: {e}"
    
    # Dapatkan informasi alamat IP
    try:
        ip_info = subprocess.run(['ip', '-4', 'addr', 'show', 'wwan0'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        ip_info = [line.split()[1] for line in ip_info.split('\n') if 'inet ' in line][0]
    except subprocess.CalledProcessError as e:
        ip_info = f"Error retrieving IP address: {e}"
    except IndexError:
        ip_info = "IP address not found"
    except FileNotFoundError as e:
        ip_info = f"ip command not found: {e}"
    
    # Dapatkan informasi gateway
    try:
        gateway_info = subprocess.run(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        gateway = [line.split()[2] for line in gateway_info.split('\n') if 'default via' in line][0]
    except subprocess.CalledProcessError as e:
        gateway = f"Error retrieving gateway: {e}"
    except IndexError:
        gateway = "Gateway not found"
    except FileNotFoundError as e:
        gateway = f"ip command not found: {e}"
    
    # Dapatkan informasi DNS
    try:
        with open('/etc/resolv.conf', 'r') as f:
            dns_lines = [line.strip() for line in f if line.startswith('nameserver')]
            dns1 = dns_lines[0].split()[1] if len(dns_lines) > 0 else "Not available"
            dns2 = dns_lines[1].split()[1] if len(dns_lines) > 1 else "Not available"
            # Filter out IPv6 loopback address
            if dns2 == "::1":
                dns2 = "Not available"
    except Exception as e:
        dns1 = dns2 = f"Error retrieving DNS info: {e}"
    
    # Dapatkan informasi koneksi aktif
    try:
        conntrack_count = subprocess.run(['cat', '/proc/sys/net/netfilter/nf_conntrack_count'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        conntrack_max = subprocess.run(['cat', '/proc/sys/net/netfilter/nf_conntrack_max'], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        active_connections = f"{conntrack_count} / {conntrack_max}"
    except subprocess.CalledProcessError as e:
        active_connections = f"Error retrieving active connections: {e}"
    except FileNotFoundError as e:
        active_connections = f"cat command not found: {e}"
    
    # Format informasi modem
    modem_info = (
        f"Protocol: {protocol}\n"
        f"Address: {ip_info}\n"
        f"Gateway: {gateway}\n"
        f"DNS 1: {dns1}\n"
        f"DNS 2: {dns2}\n"
        f"Uptime: {uptime}\n"
        f"Active Connections: {active_connections}"
    )
    
    # Kirim informasi modem kembali ke pengguna
    await update.message.reply_text(f'Modem Information\n\n{modem_info}')