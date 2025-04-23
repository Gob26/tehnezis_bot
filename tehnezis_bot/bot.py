import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from infrastructure.config import BOT_TOKEN, DATABASE_URL
from infrastructure.database.database import Base
from infrastructure.telegram_bot.handlers import handlers
from infrastructure.telegram_bot.handlers.handlers import router

load_dotenv()

dp = Dispatcher()


async def main() -> None:
    dp.include_router(handlers.router)
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")