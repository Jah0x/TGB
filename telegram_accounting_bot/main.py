import logging

from telegram import BotCommand, BotCommandScopeChat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

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

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


db = Database()


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

    return app


def main():
    app = build_application()
    app.run_polling()


if __name__ == "__main__":
    main()
