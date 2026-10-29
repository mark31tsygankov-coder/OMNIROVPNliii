import os

# Настройки бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8708312537:AAG1yrOZc5SWyl2JFXxsNQKE4ga8-Dl7ZRA")
ADMIN_IDS = [int(i) for i in os.getenv("ADMIN_IDS", "8995385837").split(",") if i.strip()]

# Названия сервиса
PROJECT_NAME = "OMNIRO VPN"

# Настройки RollyPay
ROLLYPAY_API_KEY = "Y9ZGC5UCRFgCloE-uluVczR7o12ju6GTb-oRyHaBqRk"
ROLLYPAY_SHOP_ID = "d21c4db8-e234-4a9b-a00a-2194420af7df"
ROLLYPAY_WEBHOOK_SECRET = "akjiGkcHyj6dt_WmzbSYeBBorTOnvZ1ucGQzl0BFGdk"

# Настройки H1Cloud Panel API
# Если сервер за пределами РФ: http://direct-pl7.h1cloud.net:25154/api
# Для серверов в РФ: https://s-25154.pl7.h1clayd.click/api
H1CLOUD_API_URL = os.getenv("H1CLOUD_API_URL", "https://s-25154.pl7.h1clayd.click/api")
H1CLOUD_API_TOKEN = "2ead850e5fe347fa9ed81f7838d64fc5590facdea2b94737ba7fff788bd55bb8"

# Официальные документы
POLICY_URL = "https://telegra.ph/POLITIKA-KONFIDENCIALNOSTI-08-12-99"
OFFER_URL = "https://telegra.ph/PUBLICHNAYA-OFERTA-08-12-15"
