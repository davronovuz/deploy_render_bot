from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Admin ID (Sizning ID-ingiz) va Kanal ID (Masalan: @kanal_user_name)
ADMIN_ID = 123456789
CHANNEL_ID = "@sizning_kanalingiz"


from aiogram.fsm.state import StatesGroup, State

class AdState(StatesGroup):
    name = State()      # Ism
    age = State()       # Yosh
    message = State()   # Xabar matni


# --- 1. SAVOL-JAVOBNI BOSHLASH ---
@router.message(Command("start"))
async def start_ad(message: types.Message, state: FSMContext):
    await message.answer("Xush kelibsiz! Kanalga e'lon berish uchun so'rovnomani to'ldiring.\nIsmingiz nima?")
    await state.set_state(AdState.name)


# --- 2. ISM QABUL QILISH ---
@router.message(AdState.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Yoshingiz nechida?")
    await state.set_state(AdState.age)


# --- 3. YOSH QABUL QILISH ---
@router.message(AdState.age)
async def get_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Xabaringiz mazmunini yozing:")
    await state.set_state(AdState.message)


# --- 4. XABARNI QABUL QILISH VA ADMINGA YUBORISH ---
@router.message(AdState.message)
async def get_message(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(msg=message.text)
    data = await state.get_data()  # Barcha saqlangan ma'lumotlarni olish

    await state.clear()  # Holatni tugatish
    await message.answer("Rahmat! Xabaringiz adminga yuborildi. Tasdiqlansa kanalga chiqadi.")

    # Adminga yuboriladigan Inline tugmalar
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="post_confirm"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data="post_cancel")
        ]
    ])

    full_text = (
        f"📩 <b>Yangi e'lon:</b>\n\n"
        f"👤 Ism: {data['name']}\n"
        f"🔞 Yosh: {data['age']}\n"
        f"📝 Matn: {data['msg']}"
    )

    # Adminga yuboramiz (keyinchalik callback'da ishlatish uchun matnni saqlab qoladi)
    await bot.send_message(chat_id=ADMIN_ID, text=full_text, reply_markup=keyboard, parse_mode="HTML")


# --- 5. ADMIN TASDIQLASHI ---
@router.callback_query(F.data == "post_confirm")
async def confirm_post(call: types.CallbackQuery, bot: Bot):
    # Admin tugmani bossa, xabar kanalga ketadi
    await bot.send_message(chat_id=CHANNEL_ID, text=call.message.text)
    await call.message.edit_text(f"{call.message.text}\n\n✅ <b>Kanalga chop etildi!</b>", parse_mode="HTML")
    await call.answer("Chop etildi!")


@router.callback_query(F.data == "post_cancel")
async def cancel_post(call: types.CallbackQuery):
    await call.message.edit_text(f"{call.message.text}\n\n❌ <b>Rad etildi!</b>", parse_mode="HTML")
    await call.answer("Bekor qilindi!")