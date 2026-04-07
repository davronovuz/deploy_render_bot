from aiogram import Router,types
from aiogram.filters import Command


user_router=Router()

# start buyrug'i uchun handler
@user_router.message(Command("start"))
async def start_message(message:types.Message):
    await message.answer("Hi everyone ...")




