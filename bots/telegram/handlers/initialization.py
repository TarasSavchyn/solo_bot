from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from app.models import Event, TelegramUser
from bots.telegram.keyboards import build_room_menu
from bots.telegram.states import EventStates


async def start_command(message: types.Message, state: FSMContext):
    code = message.text.split()[1] if len(message.text.split()) > 1 else None

    user, _ = await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
        },
    )

    user = await sync_to_async(
        lambda u: TelegramUser.objects.select_related("current_event").get(id=u.id)
    )(user)

    if code:
        try:
            event = await sync_to_async(Event.objects.get)(code=code)
            user.current_event = event
            await sync_to_async(user.save)()
            await state.clear()
            await message.answer(
                f"✅ Ви увійшли у кімнату: {event.name}", reply_markup=build_room_menu()
            )
            return
        except Event.DoesNotExist:
            await message.answer("❌ Івент з таким кодом не знайдено.")

    if user.current_event:
        await message.answer(
            f"🔹 Ви вже у кімнаті: {user.current_event.name}",
            reply_markup=build_room_menu(),
        )
    else:
        await state.set_state(EventStates.waiting_for_code)
        await message.answer("👋 Введіть код івенту:")


async def enter_event_code(message: types.Message, state: FSMContext):
    code = message.text.strip()
    try:
        event = await sync_to_async(Event.objects.get)(code=code)
    except Event.DoesNotExist:
        await message.answer("❌ Івент з таким кодом не знайдено. Спробуйте ще раз.")
        return

    user = await sync_to_async(TelegramUser.objects.get)(
        telegram_id=message.from_user.id
    )
    user.current_event = event
    await sync_to_async(user.save)()

    await state.clear()
    await message.answer(
        f"✅ Ви увійшли у кімнату: {event.name}", reply_markup=build_room_menu()
    )


async def leave_event_for_user(user_id: int, state: FSMContext):
    user = await sync_to_async(
        lambda: TelegramUser.objects.select_related("current_event").get(
            telegram_id=user_id
        )
    )()

    if not user.current_event:
        return None

    user.current_event = None
    await sync_to_async(user.save)()
    await state.set_state(EventStates.waiting_for_code)
    return True


async def leave_command(message: types.Message, state: FSMContext):
    result = await leave_event_for_user(message.from_user.id, state)
    if result:
        await message.answer("❌ Ви вийшли з кімнати. Введіть код нового івенту:")
    else:
        await message.answer("❌ Ви ще не в кімнаті.")


async def leave_callback(callback: types.CallbackQuery, state: FSMContext):
    result = await leave_event_for_user(callback.from_user.id, state)
    if result:
        await callback.message.answer(
            "❌ Ви вийшли з кімнати. Введіть код нового івенту:"
        )
    else:
        await callback.message.answer("❌ Ви ще не в кімнаті.")
    await callback.answer()  # закриває loading на кнопці


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
    dp.message.register(leave_command, Command(commands=["leave"]))
    dp.message.register(
        enter_event_code,
        EventStates.waiting_for_code,
        F.content_type.in_([types.ContentType.TEXT]),
    )
    dp.callback_query.register(leave_callback, lambda c: c.data == "leave_room")
