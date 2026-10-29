import aiohttp
import logging
from config import ROLLYPAY_API_KEY, ROLLYPAY_SHOP_ID

logger = logging.getLogger(__name__)

class RollyPayAPI:
    def __init__(self):
        self.api_key = ROLLYPAY_API_KEY
        self.shop_id = ROLLYPAY_SHOP_ID
        self.base_url = "https://api.rollypay.com/v1"

    async def create_bill(self, amount: float, user_id: int, order_id: str):
        payload = {
            "shop_id": self.shop_id,
            "amount": amount,
            "currency": "RUB",
            "order_id": order_id,
            "custom_fields": {"user_id": user_id}
        }
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.base_url}/bill/create", json=payload, headers=headers) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        return data.get("pay_url")
                    else:
                        logger.error(f"RollyPay error {resp.status}: {await resp.text()}")
                        return None
            except Exception as e:
                logger.error(f"RollyPay Exception: {e}")
                return None

rollypay = RollyPayAPI()
