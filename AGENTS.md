# AGENTS.md — Telegram Accounting Bot Repair Agent

## 📌 Project Summary

This is a modular Telegram accounting bot built with Python 3.12 and `python-telegram-bot v21`. It processes messages from a specific forum topic called “БУХГАЛТЕРИЯ” and stores parsed sales data in an SQLite database.

Messages look like:

```
Product Name – Price – Payment Method x3
```

The bot must:
- Parse each message
- Detect optional multipliers (x2, x3, etc...
