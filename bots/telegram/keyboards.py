from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Почати роботу")]],
    resize_keyboard=True,
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Передати фото")],
        [KeyboardButton(text="📤  Посилання на GoogleDrive з фото")],
        [KeyboardButton(text="📍 Місце проведення")],
        [KeyboardButton(text="🗳 Опитування")],
        [KeyboardButton(text="❌ Вихід в головне меню")],
    ],
    resize_keyboard=True,
)


post_upload_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Продовжити")],
        [KeyboardButton(text="🏠 Стоп / Головне меню")],
    ],
    resize_keyboard=True,
)
