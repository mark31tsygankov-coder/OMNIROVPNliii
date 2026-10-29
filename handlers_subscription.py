import datetime
import uuid
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards_main_menu import get_tariff_keyboard
from h1cloud_service import h1_client
from database import add_or_update_user, create_payment
from payment import rollypay

router = Router()

@router.callback_query(F.data == "buy_subscription")
async def show_tariffs(callback: CallbackQuery):
    text = (
        "💳 **Тарифные планы OMNIRO VPN**

"
        "🔥 **Специальное предложение — от 79 ₽!**

"
        "• **1 Месяц** — 79 ₽
"
        "• **3 Месяца** — 210 ₽ *(70 ₽/мес)*
"
        "• **1 Год** — 750 ₽ *(всего 62 ₽/мес!)*

"
        "Выберите тариф для перехода к оплате:"
    )
    await callback.message.edit_text(text, reply_markup=get_tariff_keyboard(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data.startswith("pay_"))
async def process_tariff_payment(callback: CallbackQuery):
    tariff = callback.data
    user_id = callback.from_user.id
    username = callback.from_user.username or ""
    
    days = 30
    price = 79.0
    
    if tariff == "pay_3_months":
        days = 90
        price = 210.0
    elif tariff == "pay_1_year":
        days = 365
        price = 750.0

    order_id = f"omni_{user_id}_{int(datetime.datetime.now().timestamp())}"
    create_payment(order_id, user_id, price, days)

    # Попытка получить ссылку напрямую из H1Cloud
    sub_url = await h1_client.create_or_extend_user(user_id, username, days=days)
    expire_dt = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M")

    if sub_url:
        add_or_update_user(user_id, username, callback.from_user.full_name, subscription_url=sub_url, expire_date=expire_dt)
        success_text = (
            f"🎉 **Ваш OMNIRO VPN готов!**

"
            f"⏳ Действует до: **{expire_dt}**

"
            f"🔗 **Ссылка вашей подписки:**
`{sub_url}`

"
            f"Скопируйте эту ссылку и вставьте в приложение Happ / v2rayNG / Streisand."
        )
        kbd = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="« Главное меню", callback_data="main_menu")]])
        await callback.message.edit_text(success_text, reply_markup=kbd, parse_mode="Markdown")
    else:
        # Формирование счета через RollyPay
        pay_url = await rollypay.create_bill(amount=price, user_id=user_id, order_id=order_id)
        if pay_url:
            kbd = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"💳 Оплатить {price} ₽ через RollyPay", url=pay_url)],
                [InlineKeyboardButton(text="« Назад", callback_data="buy_subscription")]
            ])
            await callback.message.edit_text("Для получения подписки оплатите счет по кнопке ниже:", reply_markup=kbd)
        else:
            await callback.message.edit_text("⚠️ Ошибка создания платежа RollyPay. Попробуйте чуть позже.")

    await callback.answer()
