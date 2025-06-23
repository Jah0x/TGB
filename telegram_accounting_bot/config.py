import os

# ID темы/чата "БУХГАЛТЕРИЯ" в которой учитываются продажи
ACCOUNTING_CHAT_ID = int(os.getenv("ACCOUNTING_CHAT_ID", "-1002242266701"))
# ID конкретной темы (thread) форума
ACCOUNTING_TOPIC_ID = int(os.getenv("ACCOUNTING_TOPIC_ID", "4294967301"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6480599695"))               # ID администратора
DB_PATH = os.getenv("DB_PATH", "accounting.db")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7311112662:AAEL_xnNZKxPxGAzSJGnKeSPivf551HqHzU")

