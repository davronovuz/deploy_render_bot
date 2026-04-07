from aiogram import Router
from aiogram import types

echo_router=Router()

@echo_router.message()
async def bot_echo(message:types.Message):
    await message.answer(message.text)