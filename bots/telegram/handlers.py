from aiogram import types
from aiogram.filters import Command

from bots.telegram.bot import dp


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Я базовий бот на aiogram 3 🚀")


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ти написав: {message.text}")