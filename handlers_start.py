from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user
from config import PROJECT_NAME

router = Router()

@router.callback_query(F.data == "my_profile")
async def show_profile(callback: CallbackQuery):
    user_data = get_user(callback.from_user.id)
    
    sub_url = user_data.get("subscription_url") if user_data else None
    expire_date = user_data.get("expire_date") if user_data else None
    
    if sub_url:
        status_str = "✅ Активна"
        sub_info = (
            f"🔗 **Ваша подписка:**\n`{sub_url}`\n\n"
            f"⏳ Действует до: **{expire_date or 'Активна'}**"
        )
    else:
        status_str = "❌ Нет подписки"
        sub_info = "У вас пока нет активного ключа."

    text = (
        f"👤 **Профиль пользователя — {PROJECT_NAME}**\n\n"
        f"🆔 Ваш ID: `{callback.from_user.id}`\n"
        f"📊 Статус: {status_str}\n\n"
        f"{sub_info}"
    )
    
    kbd = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Оформить / Продлить (от 79 ₽)", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="« Назад в меню", callback_data="main_menu")]
    ])
    
    await callback.message.edit_text(text, reply_markup=kbd, parse_mode="Markdown")
    await callback.answer()
