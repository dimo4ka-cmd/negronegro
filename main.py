import asyncio
import logging
from aiogram.bot import Bot  # Изменяем импорт
from aiogram import Dispatcher
from handlers import setup_handlers
from database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
from config import TELEGRAM_TOKEN
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Настройка обработчиков
setup_handlers(dp)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
