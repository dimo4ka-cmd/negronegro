import asyncio
import logging
from aiogram import Bot, Dispatcher  # Correct import for aiogram 3.4.1
from handlers import setup_handlers
from database import init_db

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot
from config import TELEGRAM_TOKEN
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Initialize the database
init_db()

# Set up handlers
setup_handlers(dp)

# Start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
