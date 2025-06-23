import logging
from pathlib import Path

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from .config import TELEGRAM_TOKEN, LOG_TO_FILE, LOG_FILE
from .database import Database
from .handlers.accounting import accounting_message
from .handlers.admin import addstock_cmd, setprice_cmd, getstock_cmd

def configure_logging():
    handlers = [logging.StreamHandler()]
    if LOG_TO_FILE:
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(LOG_FILE))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
    )


db = Database()


async def _init_db(app):
    await db.init()


def build_application():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .post_init(_init_db)
        .build()
    )

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, accounting_message))
    app.add_handler(CommandHandler("addstock", addstock_cmd))
    app.add_handler(CommandHandler("setprice", setprice_cmd))
    app.add_handler(CommandHandler("getstock", getstock_cmd))

    return app


def main():
    configure_logging()
    app = build_application()
    app.run_polling()


if __name__ == "__main__":
    main()
