from aiogram import Dispatcher
from aiogram import F

from asgiref.sync import sync_to_async
from aiogram.types import CallbackQuery
from app.models import TelegramUser


async def get_room_link(callback: CallbackQuery, bot=None):
    user = await sync_to_async(TelegramUser.objects.get)(
        telegram_id=callback.from_user.id
    )
    current_event = await sync_to_async(lambda: user.current_event)()

    if not current_event:
        await callback.answer("❌ Ви ще не в кімнаті.", show_alert=True)
        return

    bot_username = (await bot.get_me()).username if bot else "bot_username"
    link = f"https://t.me/{bot_username}?start={current_event.code}"

    await callback.message.answer(f"📎 Посилання на кімнату: {link}")
    await callback.answer()


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(get_room_link, F.data == "get_room_link")
