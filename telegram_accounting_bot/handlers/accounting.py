import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..config import (
    ACCOUNTING_CHAT_ID,
    ACCOUNTING_TOPIC_ID,
    ADMIN_CHAT_ID,
    SEND_EACH_SALE,
)
from ..database import Database
from ..utils.parser import parse_message
from ..utils.notifier import notify_sale


db = Database()


async def accounting_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle every text message in the accounting chat."""

    message = update.effective_message
    logging.debug("Received message: %s", message.text)

    # Обрабатываем только сообщения из нужной темы в нужном чате
    if (
        update.effective_chat.id != ACCOUNTING_CHAT_ID
        or message.message_thread_id != ACCOUNTING_TOPIC_ID
    ):
        return

    text = message.text

    try:
        product, price, payment, qty = parse_message(text)
        logging.debug(
            "Parsed: product=%s price=%s payment=%s qty=%d", product, price, payment, qty
        )
        await db.record_sale(product, price, payment, qty)
        logging.info("Sale recorded: %s (x%d)", text, qty)

        if SEND_EACH_SALE:
            await notify_sale(context.bot, product, price, payment, qty)

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


