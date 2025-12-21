from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


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
                    text="📤 Посилання на GoogleDrive з фото",
                    callback_data="get_drive_link",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Передати фото / файл", callback_data="upload_photo_file"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Вийти з кімнати", callback_data="leave_room"
                )
            ],
        ]
    )
