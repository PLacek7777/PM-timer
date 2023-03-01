import socket
import os
import ctypes

def send_message(message):
    server_address = ('0.tcp.eu.ngrok.io', 15778)  # Replace with the address of your TCP server
    header = 64
    encoding = 'utf-8'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        message_bytes = message.encode(encoding)
        message_length = len(message_bytes)
        message_header = str(message_length).encode(encoding).ljust(header)
        sock.send(message_header)
        sock.send(message_bytes)

def notify_shutdown():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    message = f"Computer {hostname} ({ip_address}) has been shut down."
    send_message(message)

def notify_startup():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    message = f"Computer {hostname} ({ip_address}) has been turned on."
    send_message(message)

def check_power_state():
    # Check if the computer is turned on or off
    system_power_status = ctypes.c_ulong()
    result = ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(system_power_status))

    if result == 0:
        notify_shutdown()

    if system_power_status.value & 0x00000001:
        pass
    else:
        notify_shutdown()

notify_startup()
while True:
    check_power_state()
