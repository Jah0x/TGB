import aiosqlite
from pathlib import Path
from typing import Optional, Tuple

from .config import DB_PATH

CREATE_TABLES_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    purchase_price REAL
);
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sale_price REAL NOT NULL,
    payment_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

class Database:
    """Async wrapper around SQLite with helper methods."""

    def __init__(self, path: str = DB_PATH):
        self.path = Path(path)

    async def init(self):
        async with aiosqlite.connect(self.path) as db:
            await db.executescript(CREATE_TABLES_SQL)
            await db.commit()

    # ---------- Product helpers ----------

    async def get_or_create_product(self, name: str) -> int:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT id FROM products WHERE name = ?", (name.strip(),))
            row = await cur.fetchone()
            if row:
                return row[0]
            cur = await db.execute("INSERT INTO products(name) VALUES (?)", (name.strip(),))
            await db.execute("INSERT INTO inventory(product_id, quantity) VALUES (?, 0)", (cur.lastrowid,))
            await db.commit()
            return cur.lastrowid

    async def set_purchase_price(self, product_name: str, price: float):
        pid = await self.get_or_create_product(product_name)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE products SET purchase_price = ? WHERE id = ?", (price, pid))
            await db.commit()

    # ---------- Inventory helpers ----------

    async def add_stock(self, product_name: str, qty: int):
        pid = await self.get_or_create_product(product_name)
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE inventory SET quantity = quantity + ? WHERE product_id = ?", (qty, pid))
            await db.commit()

    # ---------- Sales helpers ----------

    async def record_sale(self, product_name: str, price: float, payment_type: str, qty: int = 1):
        """Record a sale of *qty* units, each sold at *price* per unit."""
        pid = await self.get_or_create_product(product_name)
        async with aiosqlite.connect(self.path) as db:
            # Insert one row per unit for simplicity
            await db.executemany(
                "INSERT INTO sales(product_id, sale_price, payment_type) VALUES (?,?,?)",
                [(pid, price, payment_type)] * qty,
            )
            await db.execute("UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?", (qty, pid))
            await db.commit()

    async def get_stock(self, product_name: str) -> Optional[Tuple[int, float]]:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute(
                """
                SELECT inv.quantity, prod.purchase_price
                FROM products prod
                JOIN inventory inv ON inv.product_id = prod.id
                WHERE prod.name = ?
                """,
                (product_name.strip(),),
            )
            return await cur.fetchone()

    async def get_recent_sales(self, limit: int = 5):
        """Return last *limit* sales with product name and details."""
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute(
                """
                SELECT prod.name, s.sale_price, s.payment_type, s.created_at
                FROM sales s
                JOIN products prod ON prod.id = s.product_id
                ORDER BY s.id DESC
                LIMIT ?
                """,
                (limit,),
            )
            return await cur.fetchall()

    async def get_sales_by_date(self, date: str):
        """Return all sales for the given YYYY-MM-DD date."""
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute(
                """
                SELECT prod.name, s.sale_price, s.payment_type, s.created_at
                FROM sales s
                JOIN products prod ON prod.id = s.product_id
                WHERE date(s.created_at) = date(?)
                ORDER BY s.created_at
                """,
                (date,),
            )
            return await cur.fetchall()

