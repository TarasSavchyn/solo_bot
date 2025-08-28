import asyncio
import logging
import os

from aiogram import types
from aiogram.types import Document

from bots.google_cloude.google_cloude import gdrive

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def upload_photo(msg: types.Message, photo_obj: types.PhotoSize) -> bool:
    local_file = f"temp_{photo_obj.file_id}.jpg"
    try:
        file_info = await msg.bot.get_file(photo_obj.file_id)
        await msg.bot.download_file(file_info.file_path, local_file)
        return await asyncio.to_thread(gdrive.upload_file, local_file)
    except Exception as e:
        logger.warning(f"Failed to upload photo {photo_obj.file_id}: {e}")
        return False
    finally:
        if os.path.exists(local_file):
            try:
                os.remove(local_file)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {local_file}: {e}")


async def upload_file(msg: types.Message, doc_obj: Document) -> bool:
    local_file = f"temp_{doc_obj.file_id}_{doc_obj.file_name}"
    try:
        file_info = await msg.bot.get_file(doc_obj.file_id)
        await msg.bot.download_file(file_info.file_path, local_file)
        return await asyncio.to_thread(gdrive.upload_file, local_file)
    except Exception as e:
        logger.warning(f"Failed to upload file {doc_obj.file_id}: {e}")
        return False
    finally:
        if os.path.exists(local_file):
            try:
                os.remove(local_file)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {local_file}: {e}")
