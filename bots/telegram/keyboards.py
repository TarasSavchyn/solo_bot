from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def build_room_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Посилання на таймінг",
                    callback_data="get_timing_link",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Фото від гостей",
                    callback_data="get_drive_guests_link",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Передати фото/файл",
                    callback_data="upload_photo_file",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Фото від фотографа",
                    callback_data="get_drive_photographer_link",
                )
            ],
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
