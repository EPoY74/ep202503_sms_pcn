"""
Читаю смс сообщения из модема
"""
import time

import serial
from serial import Serial


PORT: str = "COM10"
BAUDRATE = 9600

modem: Serial = serial.Serial(PORT, BAUDRATE, timeout=1)

def send_at_commanf(command, wait_time = 1):
    modem.write((command + "\r\n").encode())
    time.sleep(wait_time)
    response = modem.read_all()
    if response is not None:
        decoded_dresponse = response.decode()
        return decoded_dresponse
    else:
        print("Ответ не получен")
        return None 