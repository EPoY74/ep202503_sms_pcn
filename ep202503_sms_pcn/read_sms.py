"""
Читаю смс сообщения из модема
"""

from operator import index
import time

import serial
from serial import Serial

PORT: str = "COM9"
BAUDRATE = 115200

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

def read_one_sms(sms_index):
    """
    чтение одной смс с индексом sms_index
    """
    send_at_command("AT+CMGF=1")
    read_sms = "AT+CMGR=" + str(sms_index)
    
    return send_at_command(read_sms)


def sms_delete(sms_index):
    """
    Удаляет смс с номером sms_index
    """
    send_at_command("AT+CMGF=1")
    del_sms = "AT+CMGD=" + str(sms_index)
    print("---")
    print(send_at_command(del_sms))
    print("---")


def sms_all_del():
    print("Deleting SMS...")
    send_at_command("AT+CMGF=1")
    send_at_command('AT+CPMS="SM"')
    print(send_at_command("AT+CMGD=1,4"))
    print("***")

def main():
    """
    Основное тело программы
    """
    # print(read_all_sms())
    # print(read_one_sms(3))
    # sms_delete(1)
    # print(read_all_sms())
    # sms_all_del()
    print(read_all_sms())

if __name__ == "__main__":
    main()
