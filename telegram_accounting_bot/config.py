import os

# ID темы/чата "БУХГАЛТЕРИЯ" в которой учитываются продажи
ACCOUNTING_CHAT_ID = int(os.getenv("ACCOUNTING_CHAT_ID", "-1002242266701"))
# ID конкретной темы (thread) форума
ACCOUNTING_TOPIC_ID = int(os.getenv("ACCOUNTING_TOPIC_ID", "4294967301"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6480599695"))               # ID администратора
DB_PATH = os.getenv("DB_PATH", "accounting.db")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7873432803:AAGs3Zlk_1sZEFHZ-qIOyvvAHoz7Wncyeiw")

# Включает отправку администратору сведений о каждой сохранённой продаже.
# Используется только во время тестирования.
SEND_EACH_SALE = bool(int(os.getenv("SEND_EACH_SALE", "0")))

# Путь до файла логов и флаг их включения
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")
LOG_TO_FILE = bool(int(os.getenv("LOG_TO_FILE", "1")))

