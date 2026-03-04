import asyncio
from aiogram import types, F, Dispatcher
from aiogram.types import (
    ContentType,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from app.models import TelegramUser
from bots.telegram.handlers.initialization import (
    enter_event_code,
    start_command,
    get_room_link,
)
from bots.telegram.keyboards import build_room_menu
from bots.telegram.states import EventStates, PhotoStates
from bots.telegram.utils import upload_file, upload_photo
from bots.google_cloude.google_cloude import gdrive

_album_cache: dict[str, list[types.Message]] = {}
_doc_cache: dict[int, list[types.Message]] = {}
ALBUM_TIMEOUT = 1.0
DOC_TIMEOUT = 1.0


async def get_event_drive_photographer_link(callback: CallbackQuery):
    user = await sync_to_async(
        TelegramUser.objects.select_related("current_event").get
    )(telegram_id=callback.from_user.id)

    event = user.current_event

    if not event:
        await callback.answer("❌ Ви ще не в кімнаті.", show_alert=True)
        return

    if not event.event_drive_photographer_link:
        await callback.answer("⏳ Фото ще не додано.", show_alert=True)
        return

    await callback.message.answer(
        f"📤 Посилання на фото від фотографа:\n{event.event_drive_photographer_link}",
        disable_web_page_preview=True,
    )
    await callback.answer()


async def get_timing_link(callback: CallbackQuery):
    user = await sync_to_async(
        TelegramUser.objects.select_related("current_event").get
    )(telegram_id=callback.from_user.id)

    event = user.current_event

    if not event:
        await callback.answer("❌ Ви ще не в кімнаті.", show_alert=True)
        return

    if not event.event_timing_link:
        await callback.answer("⏳ Таймінг ще не додано.", show_alert=True)
        return

    await callback.message.answer(
        f"📤 Посилання на таймінг:\n{event.event_timing_link}",
        disable_web_page_preview=True,
    )
    await callback.answer()


async def send_drive_link(callback: CallbackQuery):
    link = gdrive.get_folder_link()
    await callback.message.answer(
        f"📂 Посилання на папку з фото:\n{link}", disable_web_page_preview=True
    )
    await callback.answer()


async def leave_room_callback(callback: CallbackQuery, state: FSMContext):
    user = await sync_to_async(TelegramUser.objects.get)(
        telegram_id=callback.from_user.id
    )
    if not user.current_event:
        await callback.message.answer("❌ Ви ще не в кімнаті.")
        await callback.answer()
        return

    user.current_event = None
    await sync_to_async(user.save)()
    await state.set_state(EventStates.waiting_for_code)
    await callback.message.answer("❌ Ви вийшли з кімнати. Введіть код нового івенту:")
    await callback.answer()


async def ask_upload(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PhotoStates.waiting_for_photo)
    await callback.message.answer("Будь ласка, надішліть фото або файл.")
    await callback.answer()


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
    await messages_to_upload[0].reply(text, reply_markup=build_room_menu())


async def room_menu_callback(callback: CallbackQuery, state: FSMContext):
    if callback.data == "upload_photo_file":
        await ask_upload(callback, state)
    elif callback.data == "get_drive_guests_link":
        await send_drive_link(callback)
    elif callback.data == "leave_room":
        await leave_room_callback(callback, state)
    elif callback.data == "get_room_link":
        await get_room_link(callback)


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, F.text.startswith("/start"))
    dp.callback_query.register(get_timing_link, lambda c: c.data == "get_timing_link")
    dp.message.register(
        enter_event_code,
        EventStates.waiting_for_code,
        F.content_type.in_([ContentType.TEXT]),
    )
    dp.message.register(
        handle_uploads,
        PhotoStates.waiting_for_photo,
        F.content_type.in_([ContentType.PHOTO, ContentType.DOCUMENT]),
    )
    dp.callback_query.register(
        room_menu_callback,
        lambda c: c.data
        in [
            "upload_photo_file",
            "get_drive_guests_link",
            "leave_room",
            "get_room_link",
        ],
    )

    dp.callback_query.register(
        get_event_drive_photographer_link,
        lambda c: c.data == "get_drive_photographer_link",
    )
