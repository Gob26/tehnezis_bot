import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
# Local modules
from handlers.start_handlers import router as start_router
from handlers.menu_handlers import router as menu_router
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Connecting routers with handlers
dp.include_router(start_router)
dp.include_router(menu_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())