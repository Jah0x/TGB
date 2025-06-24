import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from ..config import (
    ADMIN_CHAT_ID,
    ACCOUNTING_CHAT_ID,
    ACCOUNTING_TOPIC_ID,
)
from ..database import Database


logger = logging.getLogger(__name__)


db = Database()


def _is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_CHAT_ID


async def addstock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Increase stock amount for a product."""
    if not _is_admin(update):
        return
    try:
        if len(context.args) < 2:
            raise ValueError
        *name_parts, qty_str = context.args
        product = " ".join(name_parts)
        qty = int(qty_str)
        if qty <= 0:
            raise ValueError
        await db.add_stock(product, qty)
        await update.message.reply_text(
            f"Добавлено {qty} ед. товара '{product}'."
        )
        logger.info("addstock: %s x%d", product, qty)
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Использование: /addstock <товар> <кол-во>"
        )


async def setprice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set purchase price for a product."""
    if not _is_admin(update):
        return
    try:
        if len(context.args) < 2:
            raise ValueError
        *name_parts, price_str = context.args
        product = " ".join(name_parts)
        price = float(price_str.replace(",", "."))
        if price <= 0:
            raise ValueError
        await db.set_purchase_price(product, price)
        await update.message.reply_text(
            f"Закупочная цена для '{product}' установлена: {price:.2f}"
        )
        logger.info("setprice: %s %.2f", product, price)
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Использование: /setprice <товар> <цена>"
        )
        logger.warning("setprice: invalid arguments")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка изменения цены: {exc}")
        logger.exception("setprice failed")


async def getstock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    try:
        if not context.args:
            raise ValueError
        product = " ".join(context.args)
        data = await db.get_stock(product)
        if data:
            qty, purchase_price = data
            purchase_text = (
                f"{purchase_price:.2f}" if purchase_price is not None else "не установлена"
            )
            await update.message.reply_text(
                f"Остаток '{product}': {qty} шт.; закупочная = {purchase_text}"
            )
        else:
            await update.message.reply_text("Товар не найден.")
        logger.info("getstock: %s -> %s", product, data)
    except ValueError:
        await update.message.reply_text("Использование: /getstock <товар>")
        logger.warning("getstock: no product name")
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")
        logger.exception("getstock failed")


async def send_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    await context.bot.send_message(
        ACCOUNTING_CHAT_ID,
        "привет",
        message_thread_id=ACCOUNTING_TOPIC_ID,
    )
    await update.message.reply_text("Привет отправлен.")
    logger.info("send test message")


async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    if context.args:
        date = context.args[0]
        rows = await db.get_sales_by_date(date)
    else:
        rows = await db.get_recent_sales(10)
    if rows:
        lines = [
            f"{name} - {price:.2f} - {payment} ({created_at[:16]})"
            for name, price, payment, created_at in rows
        ]
        text = "\n".join(lines)
    else:
        text = "Продажи отсутствуют."
    await update.message.reply_text(text)
    logger.info("history requested: %s", context.args[0] if context.args else "recent")


MENU_MARKUP = ReplyKeyboardMarkup(
    [
        ["/addstock", "/setprice"],
        ["/getstock", "/send"],
        ["/history", "/menu"],
    ],
    resize_keyboard=True,
)


async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    await update.message.reply_text("Выберите команду:", reply_markup=MENU_MARKUP)
    logger.info("menu shown")

