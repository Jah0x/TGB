import logging

from telegram import BotCommand, BotCommandScopeChat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, time

from .config import TELEGRAM_TOKEN, ADMIN_CHAT_ID
from .database import Database
from .handlers.accounting import accounting_message
from .handlers.admin import (
    addstock_cmd,
    setprice_cmd,
    getstock_cmd,
    send_cmd,
    history_cmd,
    menu_cmd,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


db = Database()


async def send_daily_report(context: ContextTypes.DEFAULT_TYPE):
    """Generate sales summary and send to admin."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    totals = await db.get_totals_for_date(date_str)
    await db.save_daily_report(date_str, totals)
    msg = (
        f"Отчёт за {date_str}\n"
        f"нал: {totals['нал']:.2f}\n"
        f"перевод: {totals['перевод']:.2f}\n"
        f"терминал: {totals['терминал']:.2f}"
    )
    await context.bot.send_message(ADMIN_CHAT_ID, msg)


async def _init_db(app):
    await db.init()


async def _set_admin_commands(app):
    commands = [
        BotCommand("addstock", "добавить товар на склад"),
        BotCommand("setprice", "установить закупочную цену"),
        BotCommand("getstock", "показать остаток"),
        BotCommand("send", "тестовое сообщение"),
        BotCommand("history", "история продаж"),
        BotCommand("menu", "клавиатура команд"),
    ]
    await app.bot.set_my_commands(
        commands, scope=BotCommandScopeChat(ADMIN_CHAT_ID)
    )


def build_application():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .post_init(_init_db)
        .post_init(_set_admin_commands)
        .build()
    )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, accounting_message))
    app.add_handler(CommandHandler("addstock", addstock_cmd))
    app.add_handler(CommandHandler("setprice", setprice_cmd))
    app.add_handler(CommandHandler("getstock", getstock_cmd))
    app.add_handler(CommandHandler("send", send_cmd))
    app.add_handler(CommandHandler("history", history_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))

    app.job_queue.run_daily(send_daily_report, time(hour=23, minute=0))

    return app


def main():
    app = build_application()
    app.run_polling()


if __name__ == "__main__":
    main()
