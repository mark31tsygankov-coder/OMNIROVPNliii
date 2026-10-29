from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards_main_menu import get_documents_keyboard

router = Router()

@router.callback_query(F.data == "documents")
async def show_documents(callback: CallbackQuery):
    text = (
        "⚖️ **Документы сервиса OMNIRO VPN**

"
        "Нажимая кнопки ниже, вы можете ознакомиться с официальной "
        "документацией проекта:"
    )
    await callback.message.edit_text(text, reply_markup=get_documents_keyboard(), parse_mode="Markdown")
    await callback.answer()
