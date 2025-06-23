import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..config import ACCOUNTING_CHAT_ID, ADMIN_CHAT_ID
from ..database import Database
from ..utils.parser import parse_message


db = Database()


async def accounting_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle every text message in the accounting chat."""

    if update.effective_chat.id != ACCOUNTING_CHAT_ID:
        return

    text = update.effective_message.text

    try:
        product, price, payment, qty = parse_message(text)
        await db.record_sale(product, price, payment, qty)
        logging.info("Sale recorded: %s (x%d)", text, qty)

        # alert admin if purchase price unknown
        stock_info = await db.get_stock(product)
        if stock_info and stock_info[1] is None:
            await context.bot.send_message(
                ADMIN_CHAT_ID,
                f"Для товара '{product}' не задана закупочная цена. Используйте /setprice {product} <цена>.",
            )

    except Exception as exc:
        await context.bot.send_message(
            ADMIN_CHAT_ID, f"Ошибка обработки сообщения '{text}': {exc}"
        )
        logging.exception("Parsing error")

