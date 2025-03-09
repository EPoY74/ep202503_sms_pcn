"""
Слушает модем на сом порту
"""
from time import sleep
import serial
from serial import Serial
import asyncio


port = "COM"
baudrate = 9600

try:
    modem: Serial = serial.Serial(port, baudrate, timeout=1)
except serial.SerialException as err:
    raise ValueError(f"Не удалось открыть COM-порт: {err}")

async def listen_to_modem():
    """
    Асинхронная функция для прослушивания порта
    """
    while True:
        if (modem is not None) and (modem.in_waiting >= 1):
            response = modem.read_all()
            if response:
                decoded_response = response.decode(encoding = "utf-8", errors = "strict")
                print(f"Ответ модема: {decoded_response}")
                await asyncio.sleep(0.05)