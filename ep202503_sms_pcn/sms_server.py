"""
Слушает модем на сом порту
"""
import asyncio
from datetime import datetime
import time

import serial
from serial import Serial

port = "COM9"
baudrate = 115200
modem: Serial | None= None


def now_datetime():
    """
    Возворащает текущую дату-время в формате ("%Y-%m-%d %H:%M:%S")
    """
    datetime_now = datetime.now()
    return datetime_now.strftime("%Y-%m-%d %H:%M:%S")


while True:
    try:
        modem = serial.Serial(port, baudrate, timeout=1)
        print(now_datetime(), f"Подключение успешно по {port}")
        break
    except serial.SerialException as err:
        print(now_datetime(), f"Подключение не успешно по {port}")
        time.sleep(10)





async def decode_resp(response: bytes | None ):
    if response:
        decoded_response =(
            response.decode(
                encoding = "utf-8",
                  errors = "strict").strip("\r\n^")
        )
        formatted_datetime = now_datetime()
        print(f"{formatted_datetime}: {decoded_response}")
        await asyncio.sleep(0.1)
        if decoded_response:
            return decoded_response
        else:
            return None
        

async def sms_delete(sms_index):
    """
    Удаляет смс с номером sms_index
    """
    await send_at_command("AT+CMGF=1")
    del_sms = "AT+CMGD=" + str(sms_index)
    print(f"Deleting {sms_index} SMS", await send_at_command(del_sms))


async def send_at_command(command, wait_time=1) -> str | None:
    """
    Пишет команды в модем и возврващаем ответ
    """
    if modem:
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
    await send_at_command("AT+CMGF=1")
    command_at = f"AT+CMGR={sms_index_}"
    readed_sms = await send_at_command(command_at, 1)
    return readed_sms


async def sms_split(sms_text_: str):
    sms_clean_ = sms_text_.strip().split("+CMGR: ")[1:]
    sms_parts_ = sms_clean_  #.split(",", 4)
    print(sms_parts_)
    sms_status_ = sms_parts_[0].strip('"')
    sms_inp_number_ = sms_parts_[1].strip('"')
    sms_datetime_ = sms_parts_[3].strip('"')
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
                await sms_delete(sms_index)

                if sms_content:
                    await sms_split(sms_content)

    
async def main():
    """
    основная асинхронная функция    
    """
    await send_at_command('AT+CPMS="SM"', 1)
    await listen_to_modem()


# запуск асинхронного цикла
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Программа завершена")
finally:
    if modem:
        modem.close()