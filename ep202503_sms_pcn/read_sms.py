"""
Читаю смс сообщения из модема
"""

import time

import serial
from serial import Serial

PORT: str = "COM13"
BAUDRATE = 9600

modem: Serial = serial.Serial(PORT, BAUDRATE, timeout=1)


def send_at_command(command, wait_time=1) -> str | None:
    """
    Пишет команды в модем и возврващаем ответ
    """
    modem.write((command + "\r\n").encode())
    time.sleep(wait_time)
    response = modem.read_all()
    if response is not None:
        decoded_dresponse = response.decode()
        return decoded_dresponse
    else:
        print("Ответ не получен")
        return None


def read_all_sms():
    """
    Читает все смс из модема
    """
    send_at_command("AT+CMGF=1")
    return send_at_command("AT+CMGL=\"ALL\"") #AT+CMGR 


def check_modem_resp():
    return send_at_command("AT")
        

def main():
    """
    Основное тело программы
    """
    # print(check_modem_resp())
    print(read_all_sms())
    # print(send_at_command("AT+CLAC")) # выводит все поддерживаемые команды
    

if __name__ == "__main__":
    main()
