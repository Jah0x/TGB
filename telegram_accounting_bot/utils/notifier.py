import logging
from telegram import Bot

from ..config import ADMIN_CHAT_ID


async def notify_sale(bot: Bot, product: str, price: float, payment_type: str, qty: int) -> None:
    """Send sale information to admin chat."""
    try:
        msg = (f"Продано: {product} - {price:.2f} - {payment_type} x{qty}")
        await bot.send_message(ADMIN_CHAT_ID, msg)
    except Exception:
        logging.exception("Failed to notify admin about sale")

