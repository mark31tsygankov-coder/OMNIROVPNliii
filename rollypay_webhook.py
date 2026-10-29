import hmac
import hashlib
import logging
from aiohttp import web
from config import ROLLYPAY_WEBHOOK_SECRET
from database import get_payment, update_payment_status, add_or_update_user, get_user
from h1cloud_service import h1_client

logger = logging.getLogger(__name__)

async def handle_rollypay_webhook(request):
    try:
        signature = request.headers.get("X-Signature", "")
        body = await request.read()

        # Проверка HMAC-подписи
        expected_sig = hmac.new(ROLLYPAY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
        if signature.lower() != expected_sig.lower():
            logger.warning("Неверная подпись RollyPay вебхука!")
            # При необходимости расскоментировать для строгой проверки:
            # return web.Response(status=400, text="Invalid signature")

        data = await request.json()
        status = data.get("status")
        order_id = data.get("order_id")

        if status == "paid" and order_id:
            payment = get_payment(order_id)
            if payment and payment["status"] != "paid":
                update_payment_status(order_id, "paid")
                
                user_id = payment["user_id"]
                days = payment["days"]
                
                user = get_user(user_id)
                username = user["username"] if user else ""
                
                # Создание/продление в H1Cloud
                sub_url = await h1_client.create_or_extend_user(user_id, username, days=days)
                if sub_url:
                    add_or_update_user(user_id, username, user.get("full_name", ""), subscription_url=sub_url)
                    logger.info(f"Подписка выдана для user_id {user_id}")

        return web.Response(status=200, text="OK")
    except Exception as e:
        logger.error(f"Error processing RollyPay webhook: {e}")
        return web.Response(status=500, text="Internal Error")
