"""
Слушает модем на сом порту
"""
import asyncio
#from sqlite3 import SQLITE_ERROR_MISSING_COLLSEQ

import serial
from serial import Serial

port = "COM9"
baudrate = 115200

try:
    modem: Serial = serial.Serial(port, baudrate, timeout=1)
except serial.SerialException as err:
    raise ValueError(f"Не удалось открыть COM-порт: {err}") from err


async def decode_resp(response: bytes | None ):
    if response:
        decoded_response = response.decode(encoding = "utf-8", errors = "strict")
        print(f"Ответ модема: {decoded_response}")
        await asyncio.sleep(0.1)
        if decoded_response:
            return decoded_response
        else:
            return None


async def send_at_command(command, wait_time=1) -> str | None:
    """
    Пишет команды в модем и возврващаем ответ
    """
    modem.write((command + "\r\n").encode())
    await asyncio.sleep(wait_time)
    response = modem.read_all()
    if response is not None:
        decoded_dresponse = response.decode(encoding = "utf-8", errors = "strict")
        return decoded_dresponse
    else:
        print("Ответ не получен")
        return None


async def read_sms(sms_index_: int):
    """
    Читает смс из модема с номером sms_index_
    """
    command_at = f"AT+CMGR={sms_index_}"
    readed_sms = await send_at_command(command_at, 1)
    return readed_sms


async def sms_split(sms_text_: str):
    sms_clean_ = sms_text_.strip().split("+CMGR: ")[1:]
    sms_parts_ = sms_clean_  #.split(",", 4)
    sms_status_ = sms_parts_[0].strip("\"")
    sms_inp_number_ = sms_parts_[1].strip("\"")
    sms_datetime_ = sms_parts_[3].strip("\"")
    sms_text_ = sms_parts_[4].split("\r\n")[1]

    print(sms_status_)
    print(sms_inp_number_)
    print(sms_datetime_)
    print(sms_text_)

async def listen_to_modem():
    """
    Асинхронная функция для прослушивания порта
    """
    while True:
        if (modem is not None) and (modem.in_waiting >= 1):
            response: bytes | None = modem.read_all()
            decoded_responce = await decode_resp(response)

            if decoded_responce and "+CMTI" in decoded_responce:
                sms_index: int = int(decoded_responce.split(",")[-1])
                print(f"Получено  уведомление о новой СМС с номером {sms_index}")

                sms_content = await read_sms(sms_index)
                print(f"Содержимое СМС: {sms_content}")

                if sms_content:
                    await sms_split(sms_content)

    
async def main():
    """
    основная асинхронная функция    
    """
    await listen_to_modem()


# запуск асинхронного цикла
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Программа завершена")
finally:
    modem.close()