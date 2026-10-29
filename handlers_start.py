from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import add_or_update_user
from keyboards_main_menu import get_main_keyboard
from config import PROJECT_NAME

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
    
    add_or_update_user(user_id, username, full_name)
    
    welcome_text = (
        f"🌐 **Добро пожаловать в {PROJECT_NAME}!**

"
        f"⚡ Высокоскоростной, приватный и обходящий любые блокировки VPN.
"
        f"💰 Цены всего **от 79 руб/мес**!

"
        f"Выберите нужное действие ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    welcome_text = f"🏠 **Главное меню {PROJECT_NAME}**

Выберите нужный раздел:"
    await callback.message.edit_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")
    await callback.answer()
