import os
import logging
import asyncio
from aiogram import types, Dispatcher, F
from aiogram.types import ContentType

from bots.google_cloude.google_cloude import gdrive

logger = logging.getLogger(__name__)

_album_cache: dict[str, list[types.Message]] = {}

ALBUM_TIMEOUT = 1.0


async def handle_photos(message: types.Message):
    """Handles single photo or multiple photos. Uploads them to Google Drive"""

    media_group_id = message.media_group_id

    if media_group_id:
        if media_group_id in _album_cache:
            _album_cache[media_group_id].append(message)
            return
        else:
            _album_cache[media_group_id] = [message]
            await asyncio.sleep(ALBUM_TIMEOUT)
            messages = _album_cache.pop(media_group_id)
    else:
        messages = [message]

    tasks = []

    for msg in messages:
        photo_obj = msg.photo[-1]
        local_file = f"temp_{photo_obj.file_id}.jpg"

        async def upload_task(msg=msg, photo_obj=photo_obj, local_file=local_file):
            try:
                file_info = await msg.bot.get_file(photo_obj.file_id)
                await msg.bot.download_file(file_info.file_path, local_file)
                return await asyncio.to_thread(gdrive.upload_file, local_file)
            except Exception as e:
                logger.warning(f"Failed to upload photo {photo_obj.file_id}: {e}")
                return None
            finally:
                if os.path.exists(local_file):
                    try:
                        os.remove(local_file)
                    except Exception as e:
                        logger.warning(f"Failed to delete temp file {local_file}: {e}")

        tasks.append(upload_task())

    results = await asyncio.gather(*tasks)

    if any(results):
        await messages[0].reply("✅ Your photos have been saved successfully!")
    else:
        await messages[0].reply("❌ Failed to save photos.")


def register_photo_handler(dp: Dispatcher):
    dp.message.register(handle_photos, F.content_type == ContentType.PHOTO)
