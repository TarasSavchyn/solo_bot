from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_room_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📎 Отримати посилання на кімнату",
                    callback_data="get_room_link",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Вийти з кімнати", callback_data="leave_room"
                )
            ],
        ]
    )
