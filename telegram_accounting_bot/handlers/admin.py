from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from ..config import (
    ADMIN_CHAT_ID,
    ACCOUNTING_CHAT_ID,
    ACCOUNTING_TOPIC_ID,
)
from ..database import Database


db = Database()


def _is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_CHAT_ID


async def addstock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    try:
        product = context.args[0]
        qty = int(context.args[1])
        await db.add_stock(product, qty)
        await update.message.reply_text(f"Добавлено {qty} ед. товара '{product}'.")
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /addstock <товар> <кол-во>")


async def setprice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    try:
        product = context.args[0]
        price = float(context.args[1].replace(",", "."))
        await db.set_purchase_price(product, price)
        await update.message.reply_text(
            f"Закупочная цена для '{product}' установлена: {price:.2f}"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /setprice <товар> <цена>")


async def getstock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    try:
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
    except Exception as exc:
        await update.message.reply_text(f"Ошибка: {exc}")


async def send_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_admin(update):
        return
    await context.bot.send_message(
        ACCOUNTING_CHAT_ID,
        "привет",
        message_thread_id=ACCOUNTING_TOPIC_ID,
    )
    await update.message.reply_text("Привет отправлен.")


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

