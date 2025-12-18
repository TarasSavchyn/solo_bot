import asyncio
import logging
from aiogram import types, F, Dispatcher
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext

from bots.google_cloude.google_cloude import gdrive
from bots.telegram.keyboards import start_keyboard, main_menu, post_upload_keyboard
from bots.telegram.states import PhotoStates
from bots.telegram.utils import upload_file, upload_photo

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

_album_cache: dict[str, list[types.Message]] = {}
_doc_cache: dict[int, list[types.Message]] = {}
ALBUM_TIMEOUT = 1.0
DOC_TIMEOUT = 1.0


async def send_drive_link(message: types.Message):
    link = gdrive.get_folder_link()
    await message.answer(
        f"📂 Посилання на папку з фото:\n{link}", disable_web_page_preview=True
    )


async def ask_upload(message: types.Message, state: FSMContext):
    await state.set_state(PhotoStates.waiting_for_photo)
    await message.answer("Будь ласка, надішліть фото або файл.")


async def handle_uploads(message: types.Message, state: FSMContext):
    messages_to_upload = []

    if message.content_type == ContentType.PHOTO:
        media_group_id = message.media_group_id
        if media_group_id:
            if media_group_id in _album_cache:
                _album_cache[media_group_id].append(message)
                return
            else:
                _album_cache[media_group_id] = [message]
                await asyncio.sleep(ALBUM_TIMEOUT)
                messages_to_upload = _album_cache.pop(media_group_id)
        else:
            messages_to_upload = [message]

        results = await asyncio.gather(
            *[upload_photo(msg, msg.photo[-1]) for msg in messages_to_upload]
        )

    elif message.content_type == ContentType.DOCUMENT:
        user_id = message.from_user.id
        if user_id in _doc_cache:
            _doc_cache[user_id].append(message)
            return
        else:
            _doc_cache[user_id] = [message]
            await asyncio.sleep(DOC_TIMEOUT)
            messages_to_upload = _doc_cache.pop(user_id)

        results = await asyncio.gather(
            *[upload_file(msg, msg.document) for msg in messages_to_upload]
        )

    text = (
        "✅ Ваші файли успішно збережено!"
        if any(results)
        else "❌ Не вдалося зберегти файли."
    )

    await messages_to_upload[0].reply(text, reply_markup=post_upload_keyboard)


async def post_upload_action(message: types.Message, state: FSMContext):
    if message.text == "📤 Продовжити":
        await ask_upload(message, state)
    elif message.text == "🏠 Головне меню":
        await state.clear()
        await message.answer("Головне меню:", reply_markup=main_menu)



def register_handlers(dp: Dispatcher):
    dp.message.register(ask_upload, F.text == "📤 Передати фото")
    dp.message.register(
        handle_uploads,
        PhotoStates.waiting_for_photo,
        F.content_type.in_([ContentType.PHOTO, ContentType.DOCUMENT]),
    )
    dp.message.register(
        post_upload_action, F.text.in_(["📤 Продовжити", "🏠 Головне меню"])
    )
    dp.message.register(
        send_drive_link, F.text == "📤  Посилання на GoogleDrive з фото"
    )
