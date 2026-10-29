from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == "support")
async def show_support(callback: CallbackQuery):
    text = (
        "💬 **Служба поддержки OMNIRO VPN**

"
        "Возникли вопросы по оплате, подписке или настройке? "
        "Наш саппорт на связи!"
    )
    kbd = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍💻 Связаться с поддержкой", url="https://t.me/kakooi_support")],
        [InlineKeyboardButton(text="« Назад в меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kbd, parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data == "instructions")
async def show_instructions(callback: CallbackQuery):
    text = (
        "📖 **Инструкция по подключению OMNIRO VPN**

"
        "1. Перейдите в **Профиль** и скопируйте вашу ссылку.
"
        "2. Установите приложение под ваше устройство:
"
        "   📱 **iOS**: Streisand / V2Box / Shadowrocket
"
        "   🤖 **Android**: v2rayNG / Happ
"
        "   💻 **Windows / Mac**: v2rayN / Nekoray
"
        "3. Добавьте подписку по ссылке из профиля и нажмите **Подключиться**."
    )
    kbd = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="« Назад в меню", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=kbd, parse_mode="Markdown")
    await callback.answer()
