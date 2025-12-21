import os
import django
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_agency.settings")
django.setup()

from bots.telegram.handlers.initialization import register_handlers
from bots.telegram.handlers.room_callbacks import (
    register_handlers as register_room_handlers,
)


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)

dp = Dispatcher(bot=bot)


async def main():
    register_handlers(dp)
    register_room_handlers(dp)
    logger.info("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
