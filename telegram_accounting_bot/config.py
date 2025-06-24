import os

ACCOUNTING_CHAT_ID = int(os.getenv("ACCOUNTING_CHAT_ID", "-1002242266701"))
ACCOUNTING_TOPIC_ID = int(os.getenv("ACCOUNTING_TOPIC_ID", "5"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6480599695"))               # ID администратора
DB_PATH = os.getenv("DB_PATH", "accounting.db")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7873432803:AAGs3Zlk_1sZEFHZ-qIOyvvAHoz7Wncyeiw")

# Включает отправку администратору сведений о каждой сохранённой продаже.
# Используется только во время тестирования.

/opt/tgbot/telegram_accounting_bot/config.py
