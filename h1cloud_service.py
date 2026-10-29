import aiohttp
import logging
from config import H1CLOUD_API_URL, H1CLOUD_API_TOKEN

logger = logging.getLogger(__name__)

class H1CloudAPI:
    def __init__(self):
        self.base_url = H1CLOUD_API_URL.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {H1CLOUD_API_TOKEN}",
            "Content-Type": "application/json"
        }

    async def create_or_extend_user(self, user_id: int, username: str, days: int = 30):
        user_identifier = f"omni_{user_id}"
        url = f"{self.base_url}/user"
        
        payload = {
            "username": user_identifier,
            "proxies": {"vless": {}, "vmess": {}, "trojan": {}, "shadowsocks": {}},
            "expire": days * 86400,
            "data_limit": 0,
            "note": f"OMNIRO VPN - TG ID: {user_id} (@{username})"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status in (200, 201):
                        data = await resp.json()
                        return data.get("subscription_url") or data.get("subscription_link")
                    elif resp.status == 409:
                        return await self.extend_user(user_id, days)
                    else:
                        logger.error(f"H1Cloud API Error [{resp.status}]: {await resp.text()}")
                        return None
            except Exception as e:
                logger.error(f"H1Cloud Connection Error: {e}")
                return None

    async def extend_user(self, user_id: int, days: int = 30):
        user_identifier = f"omni_{user_id}"
        url = f"{self.base_url}/user/{user_identifier}"
        
        payload = {
            "status": "active",
            "expire": days * 86400
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.put(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("subscription_url") or data.get("subscription_link")
                    else:
                        logger.error(f"H1Cloud Extend Error [{resp.status}]")
                        return None
            except Exception as e:
                logger.error(f"H1Cloud Extend Connection Error: {e}")
                return None

h1_client = H1CloudAPI()
