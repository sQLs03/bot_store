import logging
import openpyxl
import time
import os

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from main_algoritm import main_process


class FSMClient(StatesGroup):
    input_delta = State()


async def command_start(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}")
    await FSMClient.input_delta.set()
    await message.reply("Введите значение delta. Оно должно быть целочисленным.")


async def delta(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["delta"] = int(message.text)
        delta = data["delta"]
        await state.finish()
        try:
            book = openpyxl.open(os.path.join(os.getcwd(), 'file_store',
                                              os.listdir(path=os.path.join(os.getcwd(), 'file_store'))[0]),
                                 read_only=True)
            sheet = book.active
            market = 'FUTURE'
            while True:
                start_time = time.time()
                try:
                    res = main_process(delta, sheet, market)
                    await message.answer(res)
                    time.sleep(86400)
                except:
                    logging.info("Ошибка в функции main_process, 29 строка client.py")
                    await message.answer("Ошибка обработки")

        except:
            logging.error("Файл mark.xlsx не найден")
            await message.answer("Файл mark.xlsx не найден")
            await state.finish()
    except ValueError:
        logging.error(f"Было введено не int, {message.text}")
        await message.answer("Вы должны ввести целочисленное значение")
        await state.finish()


def register_handler_clients(dp: Dispatcher):
    dp.register_message_handler(command_start, CommandStart(), state=None)
    dp.register_message_handler(delta, state=FSMClient.input_delta)