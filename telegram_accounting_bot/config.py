import os

ACCOUNTING_CHAT_ID = int(os.getenv("ACCOUNTING_CHAT_ID", "-2242266701"))  # ID темы/чата "БУХГАЛТЕРИЯ"
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6480599695"))               # ID администратора
DB_PATH = os.getenv("DB_PATH", "accounting.db")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7311112662:AAEL_xnNZKxPxGAzSJGnKeSPivf551HqHzU")

