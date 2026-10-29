from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import POLICY_URL, OFFER_URL

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Подключить OMNIRO VPN", callback_data="buy_subscription")],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="my_profile"),
            InlineKeyboardButton(text="📖 Инструкция", callback_data="instructions")
        ],
        [
            InlineKeyboardButton(text="📄 Документы", callback_data="documents"),
            InlineKeyboardButton(text="💬 Поддержка", callback_data="support")
        ]
    ])

def get_documents_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔒 Политика конфиденциальности", url=POLICY_URL)],
        [InlineKeyboardButton(text="📜 Публичная оферта", url=OFFER_URL)],
        [InlineKeyboardButton(text="« Назад в меню", callback_data="main_menu")]
    ])

def get_tariff_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ 1 Месяц — 79 ₽", callback_data="pay_1_month")],
        [InlineKeyboardButton(text="⚡ 3 Месяца — 210 ₽ (70 ₽/мес)", callback_data="pay_3_months")],
        [InlineKeyboardButton(text="⚡ 1 Год — 750 ₽ (62 ₽/мес)", callback_data="pay_1_year")],
        [InlineKeyboardButton(text="« Назад", callback_data="main_menu")]
    ])
