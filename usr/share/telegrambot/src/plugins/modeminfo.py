import subprocess
import json
from telegram import Update
from telegram.ext import ContextTypes

async def modeminfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Informasi dari ubus
    try:
        ubus_output = subprocess.run(['ubus', 'call', 'network.interface.mm', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        interface_info = json.loads(ubus_output)
        protocol = interface_info.get('proto', 'Protocol information not available')
        uptime = interface_info.get('uptime', 'Uptime information not available')
        dns_servers = interface_info.get('dns-server', [])
        if isinstance(uptime, int):
            uptime = f"{uptime // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s"
    except subprocess.CalledProcessError as e:
        protocol = f"Error retrieving protocol info: {e.stderr.decode('utf-8')}"
        uptime = f"Error retrieving uptime info: {e.stderr.decode('utf-8')}"
        dns_servers = []
    except FileNotFoundError as e:
        protocol = f"ubus command not found: {e}"
        uptime = f"ubus command not found: {e}"
        dns_servers = []
    except json.JSONDecodeError as e:
        protocol = "Error decoding JSON response from ubus"
        uptime = "Error decoding JSON response from ubus"
        dns_servers = []

    # Informasi alamat IP
    try:
        ip_info = subprocess.run(['ip', '-4', 'addr', 'show', 'wwan0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        ip_info = [line.split()[1] for line in ip_info.split('\n') if 'inet ' in line][0]
    except subprocess.CalledProcessError as e:
        ip_info = f"Error retrieving IP address: {e.stderr.decode('utf-8')}"
    except IndexError:
        ip_info = "IP address not found"
    except FileNotFoundError as e:
        ip_info = f"ip command not found: {e}"

    # Informasi gateway
    try:
        gateway_info = subprocess.run(['ip', 'route', 'show', 'default'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        gateway = [line.split()[2] for line in gateway_info.split('\n') if 'default via' in line][0]
    except subprocess.CalledProcessError as e:
        gateway = f"Error retrieving gateway: {e.stderr.decode('utf-8')}"
    except IndexError:
        gateway = "Gateway not found"
    except FileNotFoundError as e:
        gateway = f"ip command not found: {e}"

    # Informasi koneksi aktif
    try:
        conntrack_count = subprocess.run(['cat', '/proc/sys/net/netfilter/nf_conntrack_count'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        conntrack_max = subprocess.run(['cat', '/proc/sys/net/netfilter/nf_conntrack_max'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        active_connections = f"{conntrack_count} / {conntrack_max}"
    except subprocess.CalledProcessError as e:
        active_connections = f"Error retrieving active connections: {e.stderr.decode('utf-8')}"
    except FileNotFoundError as e:
        active_connections = f"cat command not found: {e}"

    # Format informasi DNS
    dns1 = dns_servers[0] if len(dns_servers) > 0 else "DNS 1 not available"
    dns2 = dns_servers[1] if len(dns_servers) > 1 else "DNS 2 not available"

    # Informasi dari 3ginfo.sh
    try:
        output = subprocess.run(['/usr/share/3ginfo-lite/3ginfo.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        info = json.loads(output)
        operator_name = info.get('operator_name', 'Operator information not available')
        signal_strength = info.get('signal', 'Signal Strength information not available')
        if signal_strength != 'Signal Strength information not available':
            signal_strength += ' %'
        mode = info.get('mode', 'Mode information not available')
        registration = info.get('registration', 'Registration information not available')
        connt = info.get('connt', 'Connection time not available')
        connrx = info.get('connrx', 'Received data not available')
        conntx = info.get('conntx', 'Transmitted data not available')
        mtemp = info.get('mtemp', 'Temperature data not available')
    except subprocess.CalledProcessError as e:
        operator_name = f"Error running 3ginfo.sh: {e.stderr.decode('utf-8')}"
        signal_strength = "Signal Strength information not available"
        mode = "Mode information not available"
        registration = "Registration information not available"
        connt = "Connection time not available"
        connrx = "Received data not available"
        conntx = "Transmitted data not available"
        mtemp = "Temperature data not available"
    except json.JSONDecodeError as e:
        operator_name = "Error decoding JSON response from 3ginfo.sh"
        signal_strength = "Signal Strength information not available"
        mode = "Mode information not available"
        registration = "Registration information not available"
        connt = "Connection time not available"
        connrx = "Received data not available"
        conntx = "Transmitted data not available"
        mtemp = "Temperature data not available"
    except Exception as e:
        operator_name = f"An unexpected error occurred: {str(e)}"
        signal_strength = "Signal Strength information not available"
        mode = "Mode information not available"
        registration = "Registration information not available"
        connt = "Connection time not available"
        connrx = "Received data not available"
        conntx = "Transmitted data not available"
        mtemp = "Temperature data not available"

    # Format informasi modem
    modem_info = (
        f"Protocol: {protocol}\n"
        f"Address: {ip_info}\n"
        f"Gateway: {gateway}\n"
        f"DNS 1: {dns1}\n"
        f"DNS 2: {dns2}\n"
        f"Uptime: {uptime}\n"
        f"Active: {active_connections}\n\n"
        f"Operator: {operator_name}\n"
        f"Signal Strength: {signal_strength}\n"
        f"Mode: {mode}\n"
        f"Registration: {registration}\n"
        f"Connection Time: {connt}\n"
        f"Received Data: {connrx}\n"
        f"Transmitted Data: {conntx}\n"
        f"Temperature: {mtemp}\n"
    )

    # Kirim informasi modem kembali ke pengguna
    await update.message.reply_text(f'Modem Information\n\n{modem_info}')