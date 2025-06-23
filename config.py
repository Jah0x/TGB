import os

ACCOUNTING_CHAT_ID = int(os.getenv("ACCOUNTING_CHAT_ID", "-100123456789"))  # ID темы/чата "БУХГАЛТЕРИЯ"
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "123456789"))               # ID администратора
DB_PATH = os.getenv("DB_PATH", "accounting.db")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TOKEN_HERE")
