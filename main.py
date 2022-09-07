from aiogram.utils import executor
from loader import dp
from handlers import client


async def on_startup(_):
    print('Бот вышел в онлайн')

client.register_handler_clients(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
