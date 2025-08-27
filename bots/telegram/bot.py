import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram import F
from dotenv import load_dotenv

from bots.google_cloude.google_cloude import gdrive

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def handle_photo(message: types.Message):
    try:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        local_file = f"temp_{photo.file_id}.jpg"
        await bot.download_file(file_path, local_file)

        uploaded_file_id = gdrive.upload_file(local_file)
        os.remove(local_file)

        if uploaded_file_id:
            await message.reply(f"✅ Фото завантажено на Google Drive. ID: {uploaded_file_id}")
        else:
            await message.reply("❌ Не вдалося завантажити фото на Google Drive.")
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await message.reply(f"❌ Сталася помилка: {e}")

dp.message.register(handle_photo, F.content_type == ContentType.PHOTO)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
