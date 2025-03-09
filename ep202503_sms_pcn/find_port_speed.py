"""
Проверяю и устанавливаю скорость порта
"""

import serial
from serial import Serial

# Порт модема
port: str = "COM10"

# Список скоростей для воспроизведения
baudrates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
modem: Serial | None = None

for baudrate in baudrates:
    try:
        modem = serial.Serial(port, baudrate, timeout=1)
        modem.write(b"AT\r\n")  # test command
        response = modem.read(100)  # reading answer

        if b"OK" in response:
            print(f"Найдена правильная скорость модема: {baudrate}")
            modem.close()
            break
        else:
            print(f"Скорость {baudrate} не подходит")

    except serial.SerialException as err:
        print(f"Ошибка подключения: {err}")
    finally:
        if modem is not None:
            modem.close()
            modem = None
