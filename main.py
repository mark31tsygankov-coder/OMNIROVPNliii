import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db
from handlers_start import router as start_router
from handlers_profile import router as profile_router
from handlers_documents import router as documents_router
from handlers_subscription import router as subscription_router
from handlers_support import router as support_router

logging.basicConfig(level=logging.INFO)

async def main():
    init_db()
    
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(documents_router)
    dp.include_router(subscription_router)
    dp.include_router(support_router)
    
    logging.info("OMNIRO VPN Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
