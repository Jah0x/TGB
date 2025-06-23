import asyncio
import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from .config import TELEGRAM_TOKEN
from .database import Database
from .handlers.accounting import accounting_message
from .handlers.admin import addstock_cmd, setprice_cmd, getstock_cmd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


async def main():
    # Init DB (ensure tables exist)
    db = Database()
    await db.init()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Accounting chat messages (all text)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, accounting_message))

    # Admin commands
    app.add_handler(CommandHandler("addstock", addstock_cmd))
    app.add_handler(CommandHandler("setprice", setprice_cmd))
    app.add_handler(CommandHandler("getstock", getstock_cmd))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
