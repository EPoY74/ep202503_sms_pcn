"""
Слушает модем на сом порту
"""
import asyncio

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
        
async def read_sms(sms_index_):
    """
    Читает смс из модема с номером sms_index_
    """


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